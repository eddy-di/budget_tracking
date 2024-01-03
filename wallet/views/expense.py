from wallet.models.expense import Expense
from django.contrib.auth.models import User
from wallet.forms import EmailExpenseForm, ExpenseCommentForm, SearchForm, ExpenseAddForm
from wallet.models.wallet import Wallet

from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from taggit.models import Tag
from django.views.decorators.http import require_POST
from django.db.models import Count, Sum
from django.views.generic import ListView, CreateView
from django.core.mail import send_mail
import os
from django.contrib.postgres.search import SearchVector, \
                                           SearchQuery, SearchRank
from django.http import Http404
from django.contrib import messages
from wallet.models.sub_category import SubCategory



# class ExpenseListView(ListView):
    # """
    # Alternative way of representing the list of expenses
    # """
    # model = Expense
    # # queryset = Expense.objects.all()
    # context_object_name = 'expense'
    # paginate_by = 5
    # template_name = 'expense/list.html'



def expense_list(request, wallet_id, tag_slug=None):
    try:
        wallet = Wallet.objects.get(users=request.user, id=wallet_id)
        expense_list = Expense.objects.filter(wallet_id=wallet_id)
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            expense_list = expense_list.filter(tags__in=[tag])
        # paginating 5 elements in one page
        paginator = Paginator(expense_list, 5)
        page_number = request.GET.get('page', 1)
        try:
            expense = paginator.page(page_number)
        except PageNotAnInteger:
            expense = paginator.page(1)
        except EmptyPage:
            expense = paginator.page(paginator.num_pages)

        return render(request, 
                      'expense/list.html',
                      {'expense': expense,
                       'tag': tag,
                       'wallet': wallet})
    except Wallet.DoesNotExist:
        return Http404



@require_POST
def expense_comment(request, expense_id):
    expense = get_object_or_404(Expense,
                                 id=expense_id,
                                 currency=Expense.CurrencyChoices.KGS)
    comment = None
    # comment being sent
    form = ExpenseCommentForm(data=request.POST)
    if form.is_valid():
        # create object of class ExpenseComment, without saving it in db
        comment = form.save(commit=False)
        # # assign expense to comment
        comment.expense = expense
        # # save comment in db
        comment.save()
    
    return render(request, 'expense/comment.html',
                            {'expense': expense,
                             'form': form,
                             'comment':comment})



def expense_detail(request, wallet_id, expense_id):
    try:
        expense = get_object_or_404(Expense,
                                     currency=Expense.CurrencyChoices.KGS,
                                     id=expense_id,
                                     wallet=wallet_id)
        # number of active comments to this expense
        comments = expense.expense_comment.filter(active=True) # comments maybe need to change to expense_comment
        # form for comments
        form = ExpenseCommentForm()

        # list of similar expenses
        expense_tags_ids = expense.tags.values_list('id', flat=True)
        similar_expenses = Expense.objects.filter(tags__in=expense_tags_ids)\
                                               .exclude(id=expense.id)
        similar_expenses = similar_expenses.annotate(same_tags=Count('tags'))\
                                             .order_by('-same_tags', '-created_at')[:5]

        return render(request, 
                      'expense/detail.html',
                      {'expense': expense,
                       'comments': comments,
                       'form': form,
                       'similar_expenses': similar_expenses})
    except Wallet.DoesNotExist:
        return Http404


def expense_share(request, wallet_id, expense_id):
    user = request.user # checks if the user is logged in

    # wallet = Wallet.objects.get(users=user, id=wallet_id) # checks the m2m for user and wallet compatibility

    # get expense from its id
    expense = get_object_or_404(Expense,
                                 id=expense_id,
                                 currency=Expense.CurrencyChoices.KGS)
    
    sent = False
    
    if request.method == 'POST':
        # form was sent for handling
        form = EmailExpenseForm(request.POST)
        if form.is_valid():
            # successfully passes validation
            cd = form.cleaned_data
            # ... send email
            expense_url = request.build_absolute_uri(
                expense.get_detail_url())
            subject = f"{cd['name']} recommends you to look at " \
                      f"{expense.amount}"
            message = f"Look at {expense.amount} at {expense_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, os.environ.get('EMAIL_HOST_USER'), 
                      [cd['to']])
            sent = True
    else:
        form = EmailExpenseForm()
        
    return render(request, 'expense/share.html', {'expense': expense,
                                                  'form': form,
                                                  'sent': sent})


def expense_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('comment', 'sub_category')
            search_query = SearchQuery(query)
            results = Expense.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

    return render(request,
                  'income/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})



class AddExpenseView(CreateView):
    model = Expense
    template_name = 'expense/add_expense.html'
    fields = ['amount', 'currency', 'comment', 'sub_category', 'wallet', 'member', 'tags']


def add_expense(request, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)

    if request.method == 'POST':
        form = ExpenseAddForm(request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.member = request.user
            instance.wallet = wallet
            instance.category = form.cleaned_data['category']
            instance.sub_category = form.cleaned_data['sub_category']
            instance.save()

            messages.success(request, 'Expense saved successfully.') # success message
            return redirect('wallet:expense_list', wallet_id=wallet_id)
        else: 
            messages.error(request, 'Error saving expense.') # error message
            return render(request, 'expense/add_expense.html', {'form': form})
    else:
        form = ExpenseAddForm()
    return render(request, 'expense/add_expense.html', {'form': form})


def get_subcategories(request, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id)
    return render(request, 
                  'expense/sub_category_dropdown.html', 
                  {'subcategories': subcategories, 'wallet': wallet})


def update_subcategories(request, wallet_id, expense_id):
    wallet = Wallet.objects.get(id=wallet_id)
    expense = get_object_or_404(Expense, 
                                 id=expense_id, 
                                 wallet=wallet, 
                                 currency=Expense.CurrencyChoices.KGS)
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id)
    return render(request, 
                  'expense/sub_category_dropdown.html', 
                  {'subcategories': subcategories, 'wallet': wallet, 'expense': expense})


def update_expense(request, wallet_id, expense_id):
    wallet = Wallet.objects.get(id=wallet_id)
    expense = get_object_or_404(Expense, 
                                 id=expense_id, 
                                 wallet=wallet, 
                                 currency=Expense.CurrencyChoices.KGS)

    if request.method == 'POST':
        form = ExpenseAddForm(request.POST, instance=expense)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.member = request.user
            instance.wallet = wallet
            instance.category = form.cleaned_data['category']
            instance.sub_category = form.cleaned_data['sub_category']
            instance.save()

            messages.success(request, 'Expense updated successfully.')
            return redirect('wallet:expense_list', wallet_id=wallet_id)
        else:
            messages.error(request, 'Error updating expense.')
            return render(request, 'expense/update.html', {'form': form})
    else:
        form = ExpenseAddForm(instance=expense)

    return render(request, 
                  'expense/update.html', 
                  {'form': form, 
                   'wallet_id': wallet_id,
                   'expense':expense})


def delete_expense(request, wallet_id, expense_id):
    wallet = Wallet.objects.get(id=wallet_id)
    expense = get_object_or_404(Expense, 
                                 id=expense_id, 
                                 wallet=wallet, 
                                 currency=Expense.CurrencyChoices.KGS)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully.')
        return redirect('wallet:expense_list', wallet_id=wallet_id)

    return render(request, 
                  'expense/detail.html', 
                  {'expense': expense, 
                   'wallet_id': wallet_id})

