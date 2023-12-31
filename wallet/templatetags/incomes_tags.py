from django import template
from ..models.income import Income
from django.db.models import Count, Sum
from django.utils.safestring import mark_safe
import markdown


register = template.Library()


@register.simple_tag
def total_incomes():
    return Income.objects.count()


@register.inclusion_tag('income/latest_incomes.html')
def show_latest_incomes(count=3):
    latest_incomes = Income.objects.order_by('-created_at')[:count]
    return {'latest_incomes': latest_incomes}


@register.simple_tag
def get_most_commented_incomes(count=3):
    return Income.objects.annotate(
        total_comments=Count('income_comment')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@ register.simple_tag
def income_sum():
    return Income.objects.aggregate(Sum('amount'))['amount__sum']