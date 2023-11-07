from django.urls import path
from . import views


app_name = 'wallet'


urlpatterns = [
    # representation of wallet spending
    path('spending', views.spending_list, name='spending_list'),
    path('spending/<int:year>/<int:month>/<int:day>/<slug:spent>', 
         views.spending_detail, 
         name='spending_detail'),
    # representation of wallet earning
    path('earning', views.income_list, name='earning_list'),
    path('earning/<int:year>/<int:month>/<int:day>/<slug:earned>',
         views.income_detail, 
         name='earning_detail'),
]