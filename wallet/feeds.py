import markdown
from django.contrib.syndication.views import Feed
# from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models.spending import Spending
from .models.income import Income


class LatestSpendingsFeed(Feed):
    title = 'My spendings'
    link = reverse_lazy('wallet:spending_list')
    description = 'New spendings of the wallet'


    def items(self):
        return Spending.objects.all()[:5]
    

    def item_amount(self, item):
        return item.amount
    

    def item_created_date(self, item):
        return item.created_at
    

class LatestEarningsFeed(Feed):
    title = 'My earnings'
    link = reverse_lazy('wallet:income_list')
    description = 'New earnings of the wallet'


    def items(self):
        return Income.objects.all()[:5]
    

    def item_amount(self, item):
        return item.amount
    

    def item_created_date(self, item):
        return item.created_at