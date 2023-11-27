from django.http import Http404
from wallet.models.spending import Spending
from wallet.models.income import Income
from wallet.models.wallet import Wallet
from django.contrib.auth.models import User


from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView

def wallet_list(request): # has to show all the available wallets that the user is assigned to
    user = request.user

    wallets = Wallet.objects.filter(user=user).all()

    # wallet_url = request.build_absolute_uri(wallet.get_detail_url())

    if wallets:
        return render(request, 'wallet/wallet_index.html', {'wallets': wallets})
    else:
        return Http404




    # wallet = Wallet.objects.filter(user=user, id=wallet_id).first()


def wallet_detail(request, wallet_id):
    user = request.user

    # wallet = Wallet.objects.filter(user=user, id=wallet_id).first()

    wallet = Wallet.objects.get(id=wallet_id)

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