import os
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView, CreateView
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, \
                                           SearchQuery, SearchRank
from django.db.models import Sum

from wallet.models.income import Income
from wallet.models.spending import Spending
from wallet.models.comment_spending import SpendingComment
from wallet.models.comment_income import IncomeComment
from wallet.forms import EmailSpendingForm, IncomeCommentForm, SearchForm, EarningAddForm
from taggit.models import Tag
from wallet.models.wallet import Wallet
from django.contrib import messages
from django.contrib.auth.models import User

from django.views.decorators.http import require_POST



# class IncomeListView(ListView):
    # """
    # Alternative way of representing the list of income
    # """
    # model = Income
    # context_object_name = 'earning'
    # paginate_by = 5
    # template_name = 'income/list.html'



def income_list(request, wallet_id, tag_slug=None):
    user = request.user # checks if the user is logged in

    wallet = Wallet.objects.get(user=user, id=wallet_id) # # checks the m2m for user and wallet compatibility

    try:
        earning_list = Income.objects.filter(wallet_id=wallet_id)
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
                       'tag': tag,
                       'wallet': wallet})
    except wallet.DoesNotExist:
        return Http404



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



def income_detail(request, wallet_id, year, month, day, earned):
    user = request.user # checks if the user is logged in

    wallet = Wallet.objects.get(user=user, id=wallet_id) # # checks the m2m for user and wallet compatibility

    try:
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
    except Wallet.DoesNotExist:
        return Http404



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



class AddEarningView(CreateView):
    model = Income
    template_name = 'income/add_earning.html'
    fields = ['amount', 'currency', 'comment', 'sub_category', 'wallet', 'member', 'tags']


def add_earning(request, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = EarningAddForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.member = user
            instance.wallet = wallet
            instance.save()

            messages.success(request, 'Earning saved successfully.') # success message
            return redirect('wallet:earning_list', wallet_id=wallet_id)
        else: 
            messages.error(request, 'Error saving earning.') # error message
            return render(request, 'spending/add_spending.html', {'form': form})

    else:
        form = EarningAddForm()
    return render(request, 'spending/add_spending.html', {'form': form})


def update_earning(request, wallet_id, earning_id):
    wallet = Wallet.objects.get(id=wallet_id)
    earning = get_object_or_404(Income, 
                                 id=earning_id, 
                                 wallet=wallet, 
                                 currency=Spending.CurrencyChoices.KGS)

    if request.method == 'POST':
        form = EarningAddForm(request.POST, instance=earning)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Earning updated successfully.')
            return redirect('wallet:earning_list', wallet_id=wallet_id)
        else:
            messages.error(request, 'Error updating spending.')
            return render(request, 'income/update.html', {'form': form})
    else:
        form = EarningAddForm(instance=earning)

    return render(request, 
                  'income/update.html', 
                  {'form': form, 
                   'wallet_id': wallet_id,
                   'earning':earning})


def delete_earning(request, wallet_id, earning_id):
    wallet = Wallet.objects.get(id=wallet_id)
    earning = get_object_or_404(Income, 
                                 id=earning_id, 
                                 wallet=wallet, 
                                 currency=Spending.CurrencyChoices.KGS)

    if request.method == 'POST':
        earning.delete()
        messages.success(request, 'Earning deleted successfully.')
        return redirect('wallet:earning_list', wallet_id=wallet_id)

    return render(request, 
                  'spending/detail.html', 
                  {'earning': earning, 
                   'wallet_id': wallet_id})