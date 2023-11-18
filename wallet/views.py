import os
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView, CreateView
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, \
                                           SearchQuery, SearchRank
from django.db.models import Sum

from .models.income import Income
from .models.spending import Spending
from .models.wallet import Wallet
from .models.comment_spending import SpendingComment
from .models.comment_income import IncomeComment
from .forms import EmailSpendingForm, SpendingCommentForm, IncomeCommentForm, SearchForm
from taggit.models import Tag

from django.views.decorators.http import require_POST


# class SpendingListView(ListView):
    # """
    # Alternative way of representing the list of spendings
    # """
    # model = Spending
    # # queryset = Spending.objects.all()
    # context_object_name = 'spending'
    # paginate_by = 5
    # template_name = 'spending/list.html'

def spending_list(request, tag_slug=None):
    spending_list = Spending.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        spending_list = spending_list.filter(tags__in=[tag])
    # paginating 5 elements in one page
    paginator = Paginator(spending_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        spending = paginator.page(page_number)
    except PageNotAnInteger:
        spending = paginator.page(1)
    except EmptyPage:
        spending = paginator.page(paginator.num_pages)

    return render(request, 
                  'spending/list.html',
                  {'spending': spending,
                   'tag': tag})


@require_POST
def spending_comment(request, spending_id):
    spending = get_object_or_404(Spending,
                                 id=spending_id,
                                 currency=Spending.CurrencyChoices.KGS)
    comment = None
    # comment being sent
    form = SpendingCommentForm(data=request.POST)
    if form.is_valid():
        # create object of class SpendingComment, without saving it in db
        comment = form.save(commit=False)
        # # assign spending to comment
        comment.spending = spending
        # # save comment in db
        comment.save()
    
    return render(request, 'spending/comment.html',
                            {'spending': spending,
                             'form': form,
                             'comment':comment})


@require_POST
def income_comment(request, earning_id):
    earning = get_object_or_404(Income,
                                id=earning_id,
                                currency=Income.CurrencyChoices.KGS)
    comment = None
    form = IncomeCommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.earning = earning
        comment.save()
    return render(request, 'income/comment.html',
                            {'earning':earning,
                             'form': form,
                             'comment': comment})


def spending_detail(request, year, month, day, spent):
    spending = get_object_or_404(Spending,
                                 currency=Spending.CurrencyChoices.KGS,
                                 slug=spent,
                                 created_at__year=year,
                                 created_at__month=month,
                                 created_at__day=day,)
    # number of active comments to this spending
    comments = spending.spending_comment.filter(active=True) # comments maybe need to change to spending_comment
    # form for comments
    form = SpendingCommentForm()
    
    # list of similar spendings
    spending_tags_ids = spending.tags.values_list('id', flat=True)
    similar_spendings = Spending.objects.filter(tags__in=spending_tags_ids)\
                                           .exclude(id=spending.id)
    similar_spendings = similar_spendings.annotate(same_tags=Count('tags'))\
                                         .order_by('-same_tags', '-created_at')[:5]
    
    return render(request, 
                  'spending/detail.html',
                  {'spending': spending,
                   'comments': comments,
                   'form': form,
                   'similar_spendings': similar_spendings})


# class IncomeListView(ListView):
    # """
    # Alternative way of representing the list of income
    # """
    # model = Income
    # context_object_name = 'earning'
    # paginate_by = 5
    # template_name = 'income/list.html'


def income_list(request, tag_slug=None):
    earning_list = Income.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        earning_list = earning_list.filter(tags__in=[tag])
    # paginating 5 elements in one page
    paginator = Paginator(earning_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        earning = paginator.page(page_number)
    except PageNotAnInteger:
        earning = paginator.page(1)
    except EmptyPage:
        earning = paginator.page(paginator.num_pages)

    return render(request, 
                  'income/list.html',
                  {'earning': earning,
                   'tag': tag})

def income_detail(request, year, month, day, earned):
    earning = get_object_or_404(Income,
                                 currency=Income.CurrencyChoices.KGS,
                                 slug=earned,
                                 created_at__year=year,
                                 created_at__month=month,
                                 created_at__day=day)
    
    comments = earning.earning_comment.filter(active=True)
    form = IncomeCommentForm()

    earning_tags_ids = earning.tags.values_list('id', flat=True)
    similar_earnings = Income.objects.filter(tags__in=earning_tags_ids)\
                                           .exclude(id=earning.id)
    similar_earnings = similar_earnings.annotate(same_tags=Count('tags'))\
                                         .order_by('-same_tags', '-created_at')[:5]
    
    return render(request, 
                  'income/detail.html',
                  {'earning': earning,
                   'comments': comments,
                   'form': form,
                   'similar_earnings': similar_earnings})


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


def spending_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('comment', 'sub_category')
            search_query = SearchQuery(query)
            results = Spending.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')


    return render(request, 
                  'spending/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


def earning_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('comment', 'sub_category')
            search_query = SearchQuery(query)
            results = Income.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

    return render(request,
                  'income/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


class AddSpendingView(CreateView):
    model = Spending
    template_name = 'spending/add_spending.html'
    fields = ['amount', 'currency', 'comment', 'sub_category', 'wallet', 'member', 'tags']


class AddEarningView(CreateView):
    model = Income
    template_name = 'income/add_earning.html'
    fields = ['amount', 'currency', 'comment', 'sub_category', 'wallet', 'member', 'tags']


def wallet_info(request):
    spending_sum = Spending.objects.aggregate(Sum('amount'))['amount__sum']
    earning_sum = Income.objects.aggregate(Sum('amount'))['amount__sum']

    return render(request, 
                  'wallet/wallet.html',
                  {'spending_sum': spending_sum,
                   'earning_sum': earning_sum})