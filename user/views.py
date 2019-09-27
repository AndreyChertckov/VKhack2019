from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes
from user.models import User
from user.serializers import UserSerializer

@api_view(['POST'])
@parser_classes([JSONParser])
def create_user(request):
    data = JSONParser().parse(request)
    user = User()
    user.name = data["name"]
    user.save()
    response = HttpResponse()
    response.set_cookie('token', user.pk)
    return response

@api_view(['GET'])
def user_clock(request):
    try:
        user = User.objects.get(pk=request.COOKIES.get('token'))
    except:
        return HttpResponse(status=404)

    serializer = UserSerializer(user)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def user_logs(request):
    try:
        user = User.objects.get(pk=request.COOKIES.get('token'))
    except:
        return HttpResponse(status=404)

@api_view(['GET'])
def action_list(request):
    try:
        user = User.objects.get(pk=request.COOKIES.get('token'))
    except:
        return HttpResponse(status=404)

@api_view(['GET', 'POST'])
def action_details(request):
    try:
        user = User.objects.get(pk=request.COOKIES.get('token'))
    except:
        return HttpResponse(status=404)

@api_view(['GET'])
def user_weekly_logs(request):
    try:
        user = User.objects.get(pk=request.COOKIES.get('token'))
    except:
        return HttpResponse(status=404)

@api_view(['GET'])
def user_monthly_logs(request):
    try:
        user = User.objects.get(pk=request.COOKIES.get('token'))
    except:
        return HttpResponse(status=404)

@api_view(['GET'])
def random_fact(request):
    pass

@api_view(['GET'])
def random_fact_by_time(request):
    try:
        user = User.objects.get(pk=request.COOKIES.get('token'))
    except:
        return HttpResponse(status=404)