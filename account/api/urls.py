from django.urls import path
from . import views


app_name = 'account-api'

urlpatterns = [
    # registering
    path('register', views.RegisterView.as_view(), name='register'),
    # users
    path('users', views.UserListSerializer.as_view(), name='users'),
    path('users/<pk>/', views.UserDetailSerializer.as_view(), name='user_details'),
]