from django.urls import path
from . import views
from .feeds import LatestSpendingsFeed, LatestEarningsFeed


app_name = 'wallet'


urlpatterns = [
    # representation of wallet spending
    # path('spending', views.SpendingListView.as_view(), name='spending_list'),
    path('spending', views.spending_list, name='spending_list'),
    path('spending/<int:year>/<int:month>/<int:day>/<slug:spent>', 
         views.spending_detail, 
         name='spending_detail'),
    path('spending/<int:spending_id>/share/',
         views.spending_share, name='spending_share'),
    path('spending/<int:spending_id>/comment/',
         views.spending_comment, name='spending_comment'),
    path('spending/tag/<slug:tag_slug>/',
         views.spending_list, name='spending_list_by_tag'),
    path('spending/feed/', LatestSpendingsFeed(), name='spending_feed'),
    
    # representation of wallet earning
    # path('earning', views.IncomeListView.as_view(), name='earning_list'),
    path('earning', views.income_list, name='earning_list'),
    path('earning/<int:year>/<int:month>/<int:day>/<slug:earned>',
         views.income_detail, 
         name='earning_detail'),
    path('earning/<int:earning_id>/share/',
         views.income_share, name='income_share'),
    path('earning/<int:earning_id>/comment/',
         views.income_comment, name='earning_comment'),
    path('earning/tag/<slug:tag_slug>/',
         views.income_list, name='earning_list_by_tag'),
    path('earning/feed/', LatestEarningsFeed(), name='earning_feed'),
]