from django.urls import path
from user import views

urlpatterns = [
    path('api/user/create', views.create_empty_user),
    path('api/user/<int:user_id>', views.create_user_clock),
    path('api/user/default', views.add_token),
    path('api/user/clock', views.user_clock),
    path('api/user/logs', views.user_logs),
    path('api/action', views.action_list),
    path('api/user/logs/week', views.user_weekly_logs),
    path('api/user/logs/month', views.user_monthly_logs),
    path('api/action/<int:action_id>', views.commit_action),
    path('api/fact', views.random_fact),
    path('api/user/fact', views.random_fact_by_time)
]