from django.urls import path
from . import views


app_name = 'wallet'


urlpatterns = [
    # representation of wallet spending
    path('spending', views.SpendingListView.as_view(), name='spending_list'),
    path('spending/<int:year>/<int:month>/<int:day>/<slug:spent>', 
         views.spending_detail, 
         name='spending_detail'),
    path('spending/<int:spending_id>/share/',
         views.spending_share, name='spending_share'),
    # representation of wallet earning
    path('earning', views.IncomeListView.as_view(), name='earning_list'),
    path('earning/<int:year>/<int:month>/<int:day>/<slug:earned>',
         views.income_detail, 
         name='earning_detail'),
    path('earning/<int:earning_id>/share/',
         views.income_share, name='income_share'),
]