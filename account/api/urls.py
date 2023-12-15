from django.urls import path
from . import views


app_name = 'account-api'

urlpatterns = [
    # users
    path('users', views.UserListSerializer.as_view(), name='api_users'),
    path('users/<pk>/', views.UserDetailSerializer.as_view(), name='api_user_details'),
]