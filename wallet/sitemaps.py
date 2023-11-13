from django.contrib.sitemaps import Sitemap
from .models.spending import Spending
from .models.income import Income


class SpendingSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Spending.objects.all()
    
    def lastmod(self, obj):
        return obj.created_at
    

class IncomeSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Income.objects.all()
    
    def lastmod(self, obj):
        return obj.created_at