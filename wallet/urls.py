from django.urls import path
from . import views


app_name = 'wallet'


urlpatterns = [
    # representation of wallet
    path('', views.spending_list, name='spending_list'),
    path('<int:id>', views.spending_detail, name='spending_detail'),
]