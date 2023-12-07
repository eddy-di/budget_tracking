from django.http import Http404
from wallet.models.spending import Spending
from wallet.models.income import Income
from wallet.models.wallet import Wallet
from wallet.forms import WalletAddForm
from django.contrib.auth.models import User


from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView

def wallet_list(request): # has to show all the available wallets that the user is assigned to
    user = request.user

    wallets = Wallet.objects.filter(user=user).all()

    if wallets:
        return render(request, 'wallet/wallet_index.html', {'wallets': wallets})
    else:
        return Http404


def wallet_detail(request, wallet_id):
    user = request.user

    try:
        wallet = Wallet.objects.get(id=wallet_id)

        spending_sum = Spending.objects.filter(wallet=wallet.id).aggregate(Sum('amount'))['amount__sum'] or 0
        earning_sum = Income.objects.filter(wallet=wallet.id).aggregate(Sum('amount'))['amount__sum'] or 0
        difference = earning_sum - spending_sum

        return render(request, 
                      'wallet/wallet_detail.html',
                      {'spending_sum': spending_sum,
                       'earning_sum': earning_sum,
                       'difference': difference,
                       'wallet': wallet,
                       'user': user})
    except Wallet.DoesNotExist:
        return render(request, 'wallet/wallet_not_found.html')


def wallet_add(request):
    if request.method == "POST":
        form = WalletAddForm(request.POST)

        if form.is_valid():
            logged_user = request.user
            instance = form.save(commit=False)
            instance.save()
            instance.user.add(logged_user)
            instance.save()

        return redirect('/wallet/')
    else:
        form = WalletAddForm()
    
    return render(request, 'wallet/add.html', {'form': form})

