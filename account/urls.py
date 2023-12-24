from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'


urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('', views.account_index, name='account_index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/<str:invite_token>/', views.user_login, name='login_with_token'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
# 
    # url-адреса смены пароля
    path('password-change/',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'),
    path('password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),
# 
    # url-адреса сброса пароля
    path('password_reset/',
        auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', 
                                             email_template_name='registration/password_reset_email.html',
                                             subject_template_name='registration/password_reset_email.html',
                                             success_url=reverse_lazy('account:password_reset_done')),
        name='password_reset'),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',
                                                    success_url=reverse_lazy('account:password_reset_complete')),
        name='password_reset_confirm'),
    path('password_reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),
    # path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('register/<str:invite_token>/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('redirect/', views.redirect_to_login, name='redirect'),
    path('successful-login/', views.successful_login, name='successful_login'),
]