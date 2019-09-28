from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db.models.functions import TruncDate
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from user.models import User, Clock, Log, Action, Fact
from user.serializers import UserSerializer, ClockSerializer, LogSerializer, ActionSerializer, UserActionSerializer, FactSerializer
import datetime
from django.db.models import Sum, Q
from django.template import Template
import math


@api_view(['GET'])
def create_empty_user(request):
    data = {'name': '', 'clock': None, 'token': '', 'drinking': False, 'smoking': False}
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)

    return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
def create_user_clock(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except:
        return HttpResponse(status=404)
    received_data = JSONParser().parse(request)
    user_data = UserSerializer(user).data
    # overwrite the fields by received data
    for i in received_data.keys():
        user[i] = received_data[i]

    clock_ser = ClockSerializer(data={'time': initial_time(received_data)})
    if clock_ser.is_valid():
        clock = clock_ser.save()
        data['clock'] = clock.pk

        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)
    return JsonResponse(clock_ser.errors, status=400)


@api_view(['GET'])
def add_token(request, token):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
    except:
        return HttpResponse(status=404)

    user.token = token
    user.save()

    template = Template('Success. Token saved.')
    return template.render()


def initial_time(user_data):
    index = 0
    if user_data['heart_desease'] == True:
        index += 1
    if user_data['hypertension'] == True:
        index += 1
    if user_data['diabetes'] == True:
        index += 1
    if user_data['vascular_desease'] == True:
        index += 1
    if user_data['heridity'] == True:
        index += 1
    if user_data['smoking'] == True:
        index += 0.25
    if user_data['drinking'] == True:
        index += 0.25
    if user_data['age'] >= 65:
        if user_data['age'] >= 75:
            index += 2
        else:
            index += 1
    if user_data['sports'] == 0:
        index += 0.5
    elif user_data['sports'] == 1:
        index += 0.25
    if user_data['stress'] == 2:
        index += 0.5
    elif user_data['stress'] == 1:
        index += 0.25
    index = index / 9 * 21
    time = datetime.time(math.trunc(index), math.floor(math.fmod(index, 1)*60))
    return time


@api_view(['GET'])
def user_clock(request):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
    except:
        return HttpResponse(status=404)

    serializer = ClockSerializer(user.clock)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def user_logs(request):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
    except:
        return HttpResponse(status=404)

    serializer = LogSerializer(user.logs.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def action_list(request):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
    except:
        return HttpResponse(status=404)
    if len(user.user_actions.all()) < 1:
        serializer = ActionSerializer(Action.objects.all(), many=True)
    else:
        serializer = UserActionSerializer(user.user_actions.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@csrf_exempt
def commit_action(request, action_id):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
        action = Action.objects.get(pk=action_id)
    except:
        return HttpResponse(status=404)

    time_effect_minutes = datetime.timedelta(minutes=action.time_effect)
    new_time = (datetime.datetime.combine(datetime.date(1,1,1), user.clock.time) + time_effect_minutes).time()
    log = Log(user=user, time=datetime.datetime.now(), action=action, before=user.clock.time, after=new_time)
    user.clock.time = new_time
    user.clock.save()
    log.save()
    action.users.add(user)
    donate = False
    if user.clock.time.replace(tzinfo=None) > datetime.time(23, 0).replace(tzinfo=None):
        donate = True
    return JsonResponse({'status': 'ok', 'donate': donate})


@api_view(['GET'])
def user_weekly_logs(request):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
    except:
        return HttpResponse(status=404)

    last_7_days = datetime.datetime.today() - datetime.timedelta(7)
    logs = Log.objects.filter(user=user.pk, time__gte=last_7_days)\
        .annotate(day=TruncDate('time')).values('day').annotate(
            plus_overall=Sum('action__time_effect', filter=Q(action__time_effect__gt=0)),
            minus_overall=Sum('action__time_effect', filter=Q(action__time_effect__lt=0)))
    
    return JsonResponse(list(logs), safe=False)

@api_view(['GET'])
def user_monthly_logs(request):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
    except:
        return HttpResponse(status=404)

    last_30_days = datetime.datetime.today() - datetime.timedelta(30)
    logs = user.logs.filter(user=user.pk, time__gte=last_30_days)\
        .annotate(day=TruncDate('time')).values('day').annotate(
        plus_overall=Sum('action__time_effect', only=Q(action__time_effect__gt=0)),
        minus_overall=Sum('action__time_effect', only=Q(action__time_effect__lt=0)))

    return JsonResponse(list(logs), safe=False)


@api_view(['GET'])
def random_fact(request):
    fact = Fact.objects.order_by('?').first()
    serializer = FactSerializer(fact)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def random_fact_by_time(request):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
    except:
        return HttpResponse(status=404)
