from django.contrib.sitemaps import Sitemap
from .models.expense import Expense
from .models.income import Income


class ExpenseSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Expense.objects.all()
    
    def lastmod(self, obj):
        return obj.created_at
    

class IncomeSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Income.objects.all()
    
    def lastmod(self, obj):
        return obj.created_at