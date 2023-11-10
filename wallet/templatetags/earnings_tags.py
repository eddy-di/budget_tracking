from django import template
from ..models.income import Income
from django.db.models import Count


register = template.Library()


@register.simple_tag
def total_earnings():
    return Income.objects.count()


@register.inclusion_tag('income/latest_incomes.html')
def show_latest_earnings(count=5):
    latest_earnings = Income.objects.order_by('-created_at')[:count]
    return {'latest_earnings': latest_earnings}


@register.simple_tag
def get_most_commented_earnings(count=5):
    return Income.objects.annotate(
        total_comments=Count('earning_comment')
    ).order_by('-total_comments')[:count]