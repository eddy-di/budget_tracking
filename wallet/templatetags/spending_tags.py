from django import template
from ..models.spending import Spending
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()


@register.simple_tag
def total_spendings():
    return Spending.objects.count()


@register.inclusion_tag('spending/latest_spendings.html')
def show_latest_spendings(count=5):
    latest_spendings = Spending.objects.order_by('-created_at')[:count]
    return {'latest_spendings': latest_spendings}


@register.simple_tag
def get_most_commented_spendings(count=5):
    return Spending.objects.annotate(
        total_comments=Count('spending_comment')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))