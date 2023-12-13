from django import template
from ..models.expense import Expense
from django.db.models import Count, Sum
from django.utils.safestring import mark_safe
import markdown


register = template.Library()


@register.simple_tag
def total_expenses():

    return Expense.objects.count()


@register.inclusion_tag('expense/latest_expenses.html')
def show_latest_expenses(count=3):
    latest_expenses = Expense.objects.order_by('-created_at')[:count]
    return {'latest_expenses': latest_expenses}


@register.simple_tag
def get_most_commented_expenses(count=3):
    return Expense.objects.annotate(
        total_comments=Count('expense_comment')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def expense_sum():
    return Expense.objects.aggregate(Sum('amount'))['amount__sum']