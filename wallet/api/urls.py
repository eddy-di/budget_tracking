from django.urls import path
from . import views


app_name = 'wallet'

urlpatterns = [
    # expenses
    path('expenses', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/<pk>/', views.ExpenseDetailView.as_view(), name='expense_detail'),

    # incomes
    path('incomes', views.IncomeListView.as_view(), name='income_list'),
    path('incomes/<pk>/', views.IncomeDetailView.as_view(), name='income_detail'),

    # wallet
    path('wallets', views.WalletListView.as_view(), name='wallet_list'),
    path('wallets/<pk>/', views.WalletDetailView.as_view(), name='wallet_detail'),

]