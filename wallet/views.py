from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView

from .models.income import Income
from .models.spending import Spending


class SpendingListView(ListView):
    """
    Alternative way of representing the list of spendings
    """
    model = Spending
    context_object_name = 'spending'
    paginate_by = 5
    template_name = 'spending/list.html'

# def spending_list(request):
    # spending_list = Spending.objects.all()
    # # paginating 5 elements in one page
    # paginator = Paginator(spending_list, 5)
    # page_number = request.GET.get('page', 1)
    # try:
        # spending = paginator.page(page_number)
    # except PageNotAnInteger:
        # spending = paginator.page(1)
    # except EmptyPage:
        # spending = paginator.page(paginator.num_pages)
# 
    # return render(request, 
                #   'spending/list.html',
                #   {'spending': spending})

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


class IncomeListView(ListView):
    """
    Alternative way of representing the list of income
    """
    model = Income
    context_object_name = 'earning'
    paginate_by = 5
    template_name = 'income/list.html'


# def income_list(request):
    # earning_list = Income.objects.all()
    # # paginating 5 elements in one page
    # paginator = Paginator(earning_list, 5)
    # page_number = request.GET.get('page', 1)
    # try:
        # earning = paginator.page(page_number)
    # except PageNotAnInteger:
        # earning = paginator.page(1)
    # except EmptyPage:
        # earning = paginator.page(paginator.num_pages)
# 
    # return render(request, 
                #   'income/list.html',
                #   {'earning': earning})

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