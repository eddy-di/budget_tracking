from wallet.models.spending import Spending
from wallet.forms import EmailSpendingForm, SpendingCommentForm, SearchForm
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



# class SpendingListView(ListView):
    # """
    # Alternative way of representing the list of spendings
    # """
    # model = Spending
    # # queryset = Spending.objects.all()
    # context_object_name = 'spending'
    # paginate_by = 5
    # template_name = 'spending/list.html'



def spending_list(request, wallet_id, tag_slug=None):
    user = request.user # checks if the user is logged in

    wallet = Wallet.objects.get(user=user, id=wallet_id) # checks the m2m for user and wallet compatibility

    try:
        spending_list = Spending.objects.filter(wallet_id=wallet_id)
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
    except Wallet.DoesNotExist:
        return Http404



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



def spending_detail(request, wallet_id, spending_id):
    user = request.user # checks if the user is logged in

    wallet = Wallet.objects.get(user=user, id=wallet_id) # checks the m2m for user and wallet compatibility

    try:
        spending = get_object_or_404(Spending,
                                     currency=Spending.CurrencyChoices.KGS,
                                     id=spending_id)
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
    except Wallet.DoesNotExist:
        return Http404


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
                  'income/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})



class AddSpendingView(CreateView):
    model = Spending
    template_name = 'spending/add_spending.html'
    fields = ['amount', 'currency', 'comment', 'sub_category', 'wallet', 'member', 'tags']


