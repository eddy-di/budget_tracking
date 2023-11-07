from django.shortcuts import render, get_object_or_404

from .models.income import Income
from .models.spending import Spending


def spending_list(request):
    spending = Spending.objects.all()
    return render(request, 
                  'spending/list.html',
                  {'spending': spending})

def spending_detail(request, id):
    spending = get_object_or_404(Spending,
                                 id=id,
                                 currency=Spending.CurrencyChoices.KGS)
    
    return render(request, 
                  'spending/detail.html',
                  {'spending': spending})

def income_list(request):
    earning = Income.objects.all()
    return render(request, 
                  'income/list.html',
                  {'earning': earning})

def income_detail(request, id):
    earning = get_object_or_404(Income,
                                 id=id,
                                 currency=Income.CurrencyChoices.KGS)
    
    return render(request, 
                  'income/detail.html',
                  {'earning': earning})