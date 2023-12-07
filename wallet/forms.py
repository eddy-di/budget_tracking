from django import forms
from .models.comment_spending import SpendingComment, Spending
from .models.comment_income import IncomeComment, Income
from .models.wallet import Wallet


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


class SearchForm(forms.Form):
    query = forms.CharField()


class WalletAddForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name']


class SpendingAddForm(forms.ModelForm):
    class Meta:
        model = Spending
        exclude = ['member', 'wallet']
        fields = ['amount', 'currency', 'comment', 'sub_category']


class EarningAddForm(forms.ModelForm):
    class Meta:
        model = Income
        exclude = ['member', 'wallet']
        fields = ['amount', 'currency', 'comment', 'sub_category']