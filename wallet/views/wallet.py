from wallet.models.spending import Spending
from wallet.models.income import Income
from wallet.models.wallet import Wallet


from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView


def wallet_info(request):
    spending_sum = Spending.objects.aggregate(Sum('amount'))['amount__sum']
    earning_sum = Income.objects.aggregate(Sum('amount'))['amount__sum']

    return render(request, 
                  'wallet/wallet.html',
                  {'spending_sum': spending_sum,
                   'earning_sum': earning_sum})



class AddWalletView(CreateView):
    model = Wallet
    template_name = 'wallet/add.html'
    fields = ['name']