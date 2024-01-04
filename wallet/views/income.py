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
from wallet.models.expense import Expense
from wallet.models.comment_expense import ExpenseComment
from wallet.models.comment_income import IncomeComment
from wallet.forms import EmailExpenseForm, IncomeCommentForm, SearchForm, IncomeAddForm
from taggit.models import Tag
from wallet.models.wallet import Wallet
from django.contrib import messages
from django.contrib.auth.models import User
from wallet.models.sub_category import SubCategory

from django.views.decorators.http import require_POST



# class IncomeListView(ListView):
    # """
    # Alternative way of representing the list of income
    # """
    # model = Income
    # context_object_name = 'income'
    # paginate_by = 5
    # template_name = 'income/list.html'



def income_list(request, wallet_id, tag_slug=None):
    user = request.user # checks if the user is logged in

    wallet = Wallet.objects.get(users=user, id=wallet_id) # # checks the m2m for user and wallet compatibility

    try:
        income_list = Income.objects.filter(wallet_id=wallet_id)
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            income_list = income_list.filter(tags__in=[tag])
        # paginating 5 elements in one page
        paginator = Paginator(income_list, 5)
        page_number = request.GET.get('page', 1)
        try:
            income = paginator.page(page_number)
        except PageNotAnInteger:
            income = paginator.page(1)
        except EmptyPage:
            income = paginator.page(paginator.num_pages)

        return render(request, 
                      'income/list.html',
                      {'income': income,
                       'tag': tag,
                       'wallet': wallet})
    except wallet.DoesNotExist:
        return Http404



@require_POST
def income_comment(request, income_id):
    income = get_object_or_404(Income,
                                id=income_id,
                                currency=Income.CurrencyChoices.KGS)
    comment = None
    form = IncomeCommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.income = income
        comment.save()
    return render(request, 'income/comment.html',
                            {'income':income,
                             'form': form,
                             'comment': comment})



def income_detail(request, wallet_id, income_id):
    try:
        income = get_object_or_404(Income,
                                    currency=Income.CurrencyChoices.KGS,
                                    id=income_id,
                                    wallet=wallet_id)

        comments = income.income_comment.filter(active=True)
        form = IncomeCommentForm()

        income_tags_ids = income.tags.values_list('id', flat=True)
        similar_incomes = Income.objects.filter(tags__in=income_tags_ids)\
                                               .exclude(id=income.id)
        similar_incomes = similar_incomes.annotate(same_tags=Count('tags'))\
                                             .order_by('-same_tags', '-created_at')[:5]

        return render(request, 
                      'income/detail.html',
                      {'income': income,
                       'comments': comments,
                       'form': form,
                       'similar_incomes': similar_incomes})
    except Wallet.DoesNotExist:
        return Http404



def income_share(request, income_id):
    income = get_object_or_404(Income,
                                 id=income_id,
                                 currency=Expense.CurrencyChoices.KGS)
    
    sent=False

    if request.method == 'POST':
        # form was sent for handling
        form = EmailExpenseForm(request.POST)
        if form.is_valid():
            # successfully passes validation
            cd = form.cleaned_data
            # ... send email
            income_url = request.build_absolute_uri(
                income.get_detail_url())
            subject = f"{cd['name']} recommends you to look at " \
                      f"{income.amount}"
            message = f"Look at {income.amount} at {income_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'eddy.di.fint@gmail.com', 
                      [cd['to']])
            sent = True
    else:
        form = EmailExpenseForm()

    return render(request, 'income/share.html', {'income': income,
                                                  'form': form,
                                                  'sent': sent})



def income_search(request):
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



class AddIncomeView(CreateView):
    model = Income
    template_name = 'income/add_income.html'
    fields = ['amount', 'currency', 'comment', 'sub_category', 'wallet', 'member', 'tags']


def add_income(request, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = IncomeAddForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.category = form.cleaned_data['category']
            instance.sub_category = form.cleaned_data['sub_category']
            instance.member = request.user
            instance.wallet = wallet
            instance.save()

            messages.success(request, 'Income saved successfully.') # success message
            return redirect('wallet:income_list', wallet_id=wallet_id)
        else: 
            messages.error(request, 'Error saving income.') # error message
            return render(request, 'income/add_income.html', {'form': form})

    else:
        form = IncomeAddForm()
    return render(request, 'income/add_income.html', {'form': form})


def get_subcategories(request, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id)
    return render(request, 
                  'income/sub_category_dropdown.html', 
                  {'subcategories': subcategories, 'wallet': wallet})


def update_income(request, wallet_id, income_id):
    wallet = Wallet.objects.get(id=wallet_id)
    income = get_object_or_404(Income, 
                                 id=income_id, 
                                 wallet=wallet, 
                                 currency=Expense.CurrencyChoices.KGS)

    if request.method == 'POST':
        form = IncomeAddForm(request.POST, instance=income)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.member = request.user
            instance.wallet = wallet
            instance.category = form.cleaned_data['category']
            instance.sub_category = form.cleaned_data['sub_category']
            instance.save()

            messages.success(request, 'Income updated successfully.')
            return redirect('wallet:income_list', wallet_id=wallet_id)
        else:
            messages.error(request, 'Error updating expense.')
            return render(request, 'income/update.html', {'form': form})
    else:
        form = IncomeAddForm(instance=income)

    return render(request, 
                  'income/update.html', 
                  {'form': form, 
                   'wallet_id': wallet_id,
                   'income':income})


def update_subcategories(request, wallet_id, income_id):
    wallet = Wallet.objects.get(id=wallet_id)
    income = get_object_or_404(Income, 
                                 id=income_id, 
                                 wallet=wallet, 
                                 currency=Expense.CurrencyChoices.KGS)
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id)
    return render(request, 
                  'income/sub_category_dropdown.html', 
                  {'subcategories': subcategories, 'wallet': wallet, 'income': income})


def delete_income(request, wallet_id, income_id):
    wallet = Wallet.objects.get(id=wallet_id)
    income = get_object_or_404(Income, 
                                 id=income_id, 
                                 wallet=wallet, 
                                 currency=Expense.CurrencyChoices.KGS)

    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income deleted successfully.')
        return redirect('wallet:income_list', wallet_id=wallet_id)

    return render(request, 
                  'expense/detail.html', 
                  {'income': income, 
                   'wallet_id': wallet_id})