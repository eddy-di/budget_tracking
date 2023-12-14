from django.urls import path
from . import views
from .feeds import LatestExpensesFeed, LatestIncomesFeed


app_name = 'wallet'


urlpatterns = [
    path('', views.wallet.wallet_list, name='wallet_list'),
    path('add/', views.wallet.wallet_add, name='add_wallet'),
    path('<int:wallet_id>/', views.wallet.wallet_detail, name='wallet_info'),
    path('<int:wallet_id>/filter_by_date/', views.wallet.filter_by_date, name='filter_by_date'),


    # representation of wallet expense
    # path('expense', views.ExpenseListView.as_view(), name='expense_list'),
    path('<int:wallet_id>/expense', views.expense.expense_list, name='expense_list'),
    path('<int:wallet_id>/expense/<int:expense_id>/detail/', 
        views.expense.expense_detail, 
        name='expense_detail'),
    path('<int:wallet_id>/expense/<int:expense_id>/share/',
        views.expense.expense_share, name='expense_share'),
    path('expense/<int:expense_id>/comment/',
        views.expense.expense_comment, name='expense_comment'),
    path('expense/tag/<slug:tag_slug>/',
        views.expense.expense_list, name='expense_list_by_tag'),
    path('expense/feed/', LatestExpensesFeed(), name='expense_feed'),
    path('expense/search/', views.expense.expense_search, name='expense_search'),
    path('<int:wallet_id>/expense/add/', views.expense.add_expense, name='add_expense'),
    path('<int:wallet_id>/expense/add/get_subcategories/', 
         views.expense.get_subcategories, name='get_subcategories'),
    path('<int:wallet_id>/expense/<int:expense_id>/update/', 
         views.expense.update_expense, name='update_expense'),
    path('<int:wallet_id>/expense/<int:expense_id>/update/get_subcategories/', 
         views.expense.update_subcategories, name='get_subcategories_update'),
    path('<int:wallet_id>/expense/<int:expense_id>/delete/', 
         views.expense.delete_expense, name='delete_expense'),
    

    # representation of wallet income
    # path('income', views.income.IncomeListView.as_view(), name='income_list'),
    path('<int:wallet_id>/income', views.income.income_list, name='income_list'),
    path('<int:wallet_id>/income/<slug:earned>/<int:year>/<int:month>/<int:day>',
        views.income.income_detail, 
        name='income_detail'),
    path('income/<int:income_id>/share/',
        views.income.income_share, name='income_share'),
    path('income/<int:income_id>/comment/',
        views.income.income_comment, name='income_comment'),
    path('income/tag/<slug:tag_slug>/',
        views.income.income_list, name='income_list_by_tag'),
    path('income/feed/', LatestIncomesFeed(), name='income_feed'),
    path('income/search/', views.income.income_search, name='income_search'),
    path('<int:wallet_id>/income/add/', views.income.add_income, name='add_income'),
    path('<int:wallet_id>/income/add/get_subcategories/', 
         views.income.get_subcategories, name='get_subcategories'),
    path('<int:wallet_id>/income/<int:income_id>/update/', 
         views.income.update_income, name='update_income'),
    path('<int:wallet_id>/income/<int:income_id>/update/get_subcategories/', 
        views.income.update_subcategories, name='get_subcategories_update'),
    path('<int:wallet_id>/income/<int:income_id>/delete/', views.income.delete_income, name='delete_income'),
]