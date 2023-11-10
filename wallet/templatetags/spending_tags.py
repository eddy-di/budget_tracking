from django import template
from ..models.spending import Spending


register = template.Library()


@register.simple_tag
def total_spendings():
    return Spending.objects.count()


@register.inclusion_tag('spending/latest_spendings.html')
def show_latest_spendings(count=5):
    latest_spendings = Spending.objects.order_by('-created_at')[:count]
    return {'latest_spendings': latest_spendings}