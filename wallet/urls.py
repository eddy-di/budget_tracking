from django.urls import path
from . import views
from .feeds import LatestSpendingsFeed, LatestEarningsFeed


app_name = 'wallet'


urlpatterns = [
    path('', views.wallet.wallet_info, name='wallet_info'),
    path('add/', views.wallet.AddWalletView.as_view(), name='add_wallet'),
    # representation of wallet spending
    # path('spending', views.SpendingListView.as_view(), name='spending_list'),
    path('spending', views.spending.spending_list, name='spending_list'),
    path('spending/<slug:spent>/<int:year>/<int:month>/<int:day>', 
        views.spending.spending_detail, 
        name='spending_detail'),
    path('spending/<int:spending_id>/share/',
        views.spending.spending_share, name='spending_share'),
    path('spending/<int:spending_id>/comment/',
        views.spending.spending_comment, name='spending_comment'),
    path('spending/tag/<slug:tag_slug>/',
        views.spending.spending_list, name='spending_list_by_tag'),
    path('spending/feed/', LatestSpendingsFeed(), name='spending_feed'),
    path('spending/search/', views.spending.spending_search, name='spending_search'),
    path('spending/add/', views.spending.AddSpendingView.as_view(), name='add_spending'),
    
    # representation of wallet earning
    # path('earning', views.earning.IncomeListView.as_view(), name='earning_list'),
    path('earning', views.earning.income_list, name='earning_list'),
    path('earning/<slug:earned>/<int:year>/<int:month>/<int:day>',
        views.earning.income_detail, 
        name='earning_detail'),
    path('earning/<int:earning_id>/share/',
        views.earning.income_share, name='income_share'),
    path('earning/<int:earning_id>/comment/',
        views.earning.income_comment, name='earning_comment'),
    path('earning/tag/<slug:tag_slug>/',
        views.earning.income_list, name='earning_list_by_tag'),
    path('earning/feed/', LatestEarningsFeed(), name='earning_feed'),
    path('earning/search/', views.earning.earning_search, name='earning_search'),
    path('earning/add/', views.earning.AddEarningView.as_view(), name='add_earning'),
]