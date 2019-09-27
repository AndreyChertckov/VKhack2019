from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from user.models import User
from user.serializers import UserSerializer

# return json {current: time, plus: time, minus: time}
def user_clock(request):
    try:
        user = User.objects.get(pk=request.COOKIES.get('token'))
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # get logs of the user for the day
        # compute plus and minus
        # build json
        # return
        pass

def user_logs(request):
    try:
        user = User.objects.get(pk=request.COOKIES.get('token'))
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # get logs of the user
        # compute before and after time of each log
        # build json
        # return
        pass

def user_weekly_logs(request):
    try:
        user = User.objects.get(pk=request.COOKIES.get('token'))
    except:
        return HttpResponse(status=404)

def user_monthly_logs(request):
    try:
        user = User.objects.get(pk=request.COOKIES.get('token'))
    except:
        return HttpResponse(status=404)

        
    
