from django.http import Http404
from wallet.models.expense import Expense
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

        expense_sum = Expense.objects.filter(wallet=wallet.id).aggregate(Sum('amount'))['amount__sum'] or 0
        income_sum = Income.objects.filter(wallet=wallet.id).aggregate(Sum('amount'))['amount__sum'] or 0
        difference = income_sum - expense_sum

        data = [str(expense_sum), str(income_sum)]
        # labels = ['Expenses', 'Incomes']
        expenses = Expense.objects.filter(wallet=wallet).values_list('amount', 'category__name', 'sub_category__name')
        incomes = Income.objects.filter(wallet=wallet).values_list('amount', 'category__name', 'sub_category__name')
        expenses_categories_d = {}
        # getting expense sums based on categories and summing them by amount
        for i in list(expenses):
            if i[1] not in expenses_categories_d:
                expenses_categories_d[i[1]] = i[0]
            else:
                expenses_categories_d[i[1]] += i[0]
        # getting expense sums based on sub_categories and summing them by amount
        expenses_subcats_d = {}
        for i in list(expenses):
            if i[2] not in expenses_subcats_d:
                expenses_subcats_d[i[2]] = i[0]
            else:
                expenses_subcats_d[i[2]] += i[0]
        # getting income sums based on categories and summing them by amount
        income_subcategories_d = {}
        for i in list(incomes):
            if i[2] not in income_subcategories_d:
                income_subcategories_d[i[2]] = i[0]
            else:
                income_subcategories_d[i[2]] += i[0]
        
        data_expenses_category = [ str(v) for v in expenses_categories_d.values() ]
        labels_expenses_category = [k for k in expenses_categories_d.keys()]

        data_incomes_subcategory = [ str(v) for v in income_subcategories_d.values() ]
        labels_incomes_subcategory = [k for k in income_subcategories_d.keys()]


        return render(request, 
                      'wallet/wallet_detail.html',
                      {'expense_sum': expense_sum,
                       'income_sum': income_sum,
                       'difference': difference,
                       'wallet': wallet,
                       'user': user,
                       'data': data,
                       'data_expenses_category': data_expenses_category,
                       'labels_expenses_category': labels_expenses_category,
                       'data_incomes_subcategory': data_incomes_subcategory,
                       'labels_incomes_subcategory': labels_incomes_subcategory
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

