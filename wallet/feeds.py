import markdown
from django.contrib.syndication.views import Feed
# from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models.expense import Expense
from .models.income import Income


class LatestExpensesFeed(Feed):
    title = 'My expenses'
    link = reverse_lazy('wallet:expense_list')
    description = 'New expenses of the wallet'


    def items(self):
        return Expense.objects.all()[:5]
    

    def item_amount(self, item):
        return item.amount
    

    def item_created_date(self, item):
        return item.created_at
    

class LatestIncomesFeed(Feed):
    title = 'My incomes'
    link = reverse_lazy('wallet:income_list')
    description = 'New incomes of the wallet'


    def items(self):
        return Income.objects.all()[:5]
    

    def item_amount(self, item):
        return item.amount
    

    def item_created_date(self, item):
        return item.created_at