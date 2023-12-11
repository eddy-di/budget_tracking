from django.http import Http404
from wallet.models.spending import Spending
from wallet.models.income import Income
from wallet.models.wallet import Wallet
from wallet.models.category  import Category
from wallet.models.sub_category import SubCategory
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
    cats = Category.objects.all()
    subcats = SubCategory.objects.all()

    try:
        wallet = Wallet.objects.get(id=wallet_id)

        spending_sum = Spending.objects.filter(wallet=wallet.id).aggregate(Sum('amount'))['amount__sum'] or 0
        earning_sum = Income.objects.filter(wallet=wallet.id).aggregate(Sum('amount'))['amount__sum'] or 0
        difference = earning_sum - spending_sum

        data = [str(spending_sum), str(earning_sum)]
        # labels = ['Spendings', 'Earnings']
        spendings = Spending.objects.filter(wallet=wallet).values_list('amount', 'category__category_name', 'sub_category__sub_category_name')
        earnings = Income.objects.filter(wallet=wallet).values_list('amount', 'category__category_name', 'sub_category__sub_category_name')
        spendings_categories_d = {}
        # getting spending sums based on categories and summing them by amount
        for i in list(spendings):
            if i[1] not in spendings_categories_d:
                spendings_categories_d[i[1]] = i[0]
            else:
                spendings_categories_d[i[1]] += i[0]
        # getting spending sums based on sub_categories and summing them by amount
        spendings_subcats_d = {}
        for i in list(spendings):
            if i[2] not in spendings_subcats_d:
                spendings_subcats_d[i[2]] = i[0]
            else:
                spendings_subcats_d[i[2]] += i[0]
        # getting earning sums based on categories and summing them by amount
        earning_subcategories_d = {}
        for i in list(earnings):
            if i[2] not in earning_subcategories_d:
                earning_subcategories_d[i[2]] = i[0]
            else:
                earning_subcategories_d[i[2]] += i[0]
        
        data_spendings_category = [ str(v) for v in spendings_categories_d.values() ]
        labels_spendings_category = [k for k in spendings_categories_d.keys()]

        data_earnings_subcategory = [ str(v) for v in earning_subcategories_d.values() ]
        labels_earnings_subcategory = [k for k in earning_subcategories_d.keys()]


        return render(request, 
                      'wallet/wallet_detail.html',
                      {'spending_sum': spending_sum,
                       'earning_sum': earning_sum,
                       'difference': difference,
                       'wallet': wallet,
                       'user': user,
                       'data': data,
                       'data_spendings_category': data_spendings_category,
                       'labels_spendings_category': labels_spendings_category,
                       'data_earnings_subcategory': data_earnings_subcategory,
                       'labels_earnings_subcategory': labels_earnings_subcategory
                       }) # 'labels': labels
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

