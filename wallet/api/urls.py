from django.urls import path
from . import views


app_name = 'wallet'

urlpatterns = [
    # spendings
    path('spendings', views.SpendingListView.as_view(), name='spending_list'),
    path('spendings/<pk>/', views.SpendingDetailView.as_view(), name='spending_detail'),

    # earnings
    path('earnings', views.EarningListView.as_view(), name='earning_list'),
    path('earnings/<pk>/', views.EarningDetailView.as_view(), name='earning_detail'),

    # wallet
    path('wallets', views.WalletListView.as_view(), name='wallet_list'),
    path('wallets/<pk>/', views.WalletDetailView.as_view(), name='wallet_detail'),

]