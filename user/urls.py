from django.urls import path
from user import views

urlpatterns = [
    path('api/user', views.create_user),
    path('api/user/clock', views.user_clock),
    path('api/user/logs', views.user_logs),
    path('api/action', views.action_list),
    path('api/user/logs/week', views.user_weekly_logs)
]