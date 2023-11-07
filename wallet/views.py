from django.shortcuts import render, get_object_or_404

from .models.income import Income
from .models.spending import Spending


def spending_list(request):
    spending = Spending.objects.all()
    return render(request, 
                  'spending/list.html',
                  {'spending': spending})

def spending_detail(request, year, month, day, spent):
    spending = get_object_or_404(Spending,
                                 currency=Spending.CurrencyChoices.KGS,
                                 slug=spent,
                                 created_at__year=year,
                                 created_at__month=month,
                                 created_at__day=day)
    
    return render(request, 
                  'spending/detail.html',
                  {'spending': spending})

def income_list(request):
    earning = Income.objects.all()
    return render(request, 
                  'income/list.html',
                  {'earning': earning})

def income_detail(request, year, month, day, earned):
    earning = get_object_or_404(Income,
                                 currency=Income.CurrencyChoices.KGS,
                                 slug=earned,
                                 created_at__year=year,
                                 created_at__month=month,
                                 created_at__day=day)
    
    return render(request, 
                  'income/detail.html',
                  {'earning': earning})