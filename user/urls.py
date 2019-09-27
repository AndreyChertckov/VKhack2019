from django.urls import path
from user import views

urlpatterns = [
    path('api/user/clock', views.user_clock),
    path('api/user', views.create_user)
]