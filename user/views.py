from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes
from user.models import User, Clock, Log
from user.serializers import UserSerializer, ClockSerializer, LogSerializer, ActionSerializer, UserActionSerializer
import datetime

@api_view(['POST'])
@parser_classes([JSONParser])
def create_user(request):
    data = JSONParser().parse(request)

    clock_ser = ClockSerializer(data={'time': datetime.time(12, 10)})
    if clock_ser.is_valid():
        clock = clock_ser.save()
        data['clock'] = clock.pk

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
    
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse(clock_ser.errors, status=400)

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

    serializer = UserActionSerializer(user.user_actions.all(), many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET', 'POST'])
def action_details(request):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
    except:
        return HttpResponse(status=404)

@api_view(['GET'])
def user_weekly_logs(request):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
    except:
        return HttpResponse(status=404)

@api_view(['GET'])
def user_monthly_logs(request):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
    except:
        return HttpResponse(status=404)

@api_view(['GET'])
def random_fact(request):
    pass

@api_view(['GET'])
def random_fact_by_time(request):
    try:
        user = User.objects.get(pk=request.GET.get('token'))
    except:
        return HttpResponse(status=404)