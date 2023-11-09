from django import forms
from .models.comment_spending import SpendingComment
from .models.comment_income import IncomeComment


class EmailSpendingForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SpendingCommentForm(forms.ModelForm):
    class Meta:
        model = SpendingComment
        fields = ['name', 'email', 'body']


class IncomeCommentForm(forms.ModelForm):
    class Meta:
        model = IncomeComment
        fields = ['name', 'email', 'body']
