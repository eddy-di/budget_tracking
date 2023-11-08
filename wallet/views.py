import os
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from .models.income import Income
from .models.spending import Spending
from .forms import EmailSpendingForm


class SpendingListView(ListView):
    """
    Alternative way of representing the list of spendings
    """
    model = Spending
    # queryset = Spending.objects.all()
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


def spending_share(request, spending_id):
    # get spending from its id
    spending = get_object_or_404(Spending,
                                 id=spending_id,
                                 currency=Spending.CurrencyChoices.KGS)
    
    sent = False
    
    if request.method == 'POST':
        # form was sent for handling
        form = EmailSpendingForm(request.POST)
        if form.is_valid():
            # successfully passes validation
            cd = form.cleaned_data
            # ... send email
            spending_url = request.build_absolute_uri(
                spending.get_absolute_url())
            subject = f"{cd['name']} recommends you to look at " \
                      f"{spending.amount}"
            message = f"Look at {spending.amount} at {spending_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, os.environ.get('EMAIL_HOST_USER'), 
                      [cd['to']])
            sent = True
    else:
        form = EmailSpendingForm()
    
    return render(request, 'spending/share.html', {'spending': spending,
                                                  'form': form,
                                                  'sent': sent})


def income_share(request, earning_id):
    earning = get_object_or_404(Income,
                                 id=earning_id,
                                 currency=Spending.CurrencyChoices.KGS)
    
    sent=False

    if request.method == 'POST':
        # form was sent for handling
        form = EmailSpendingForm(request.POST)
        if form.is_valid():
            # successfully passes validation
            cd = form.cleaned_data
            # ... send email
            earning_url = request.build_absolute_uri(
                earning.get_absolute_url())
            subject = f"{cd['name']} recommends you to look at " \
                      f"{earning.amount}"
            message = f"Look at {earning.amount} at {earning_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'eddy.di.fint@gmail.com', 
                      [cd['to']])
            sent = True
    else:
        form = EmailSpendingForm()

    return render(request, 'income/share.html', {'earning': earning,
                                                  'form': form,
                                                  'sent': sent})

