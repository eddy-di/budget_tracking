from wallet.models.spending import Spending
from wallet.models.income import Income
from wallet.models.wallet import Wallet


from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView

def wallet_index(request):
    user = request.user

    wallet = Wallet.objects.filter(user=user)

    if wallet:
        return render(request, 'wallet/wallet_index.html', {'wallet': wallet})
    else:
        add_link = 'wallet/add.html'



    # wallet = Wallet.objects.filter(user=user, id=wallet_id).first()


def wallet_detail(request, wallet_id):
    user = request.user

    wallet = Wallet.objects.filter(user=user, id=wallet_id).first()

    if wallet:
        spending_sum = Spending.objects.aggregate(Sum('amount'))['amount__sum']
        earning_sum = Income.objects.aggregate(Sum('amount'))['amount__sum']
        difference = earning_sum - spending_sum

        return render(request, 
                      'wallet/wallet_detail.html',
                      {'spending_sum': spending_sum,
                       'earning_sum': earning_sum,
                       'difference': difference,
                       'wallet': wallet,
                       'user': user})
    else:
        return render(request, 'wallet/wallet_not_found.html')



class AddWalletView(CreateView):
    model = Wallet
    template_name = 'wallet/add.html'
    fields = ['name']