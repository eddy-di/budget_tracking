from django import forms
from .models.comment_spending import SpendingComment, Spending
from .models.comment_income import IncomeComment, Income
from .models.wallet import Wallet
from .models.sub_category import SubCategory
from .models.category import Category


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
    category = forms.ModelChoiceField(queryset=Category.objects.all(), 
                                      widget=forms.Select(attrs={'hx-get': 'get_subcategories/', 
                                                                 'hx-target': '#id_sub_category'}))
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.none())

    class Meta:
        model = Spending
        exclude = ['member', 'wallet']
        fields = ['amount', 'currency', 'comment']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Check if 'category' is in the form's data
        if 'category' in self.data:
            category_id = int(self.data.get('category'))
            # Update the queryset for 'sub_category' based on the selected category
            self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id)
        elif self.instance.pk:
            # If updating an existing spending, set the queryset based on the existing category
            self.initial['category'] = self.instance.category.pk
            self.fields['sub_category'].queryset = self.instance.category.subcategory_set.all()



class EarningAddForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), 
                                      widget=forms.Select(attrs={'hx-get': 'get_subcategories/', 
                                                                 'hx-target': '#id_sub_category'}))
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.none())

    class Meta:
        model = Income
        exclude = ['member', 'wallet']
        fields = ['amount', 'currency', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Check if 'category' is in the form's data
        if 'category' in self.data:
            category_id = int(self.data.get('category'))
            # Update the queryset for 'sub_category' based on the selected category
            self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id)
        elif self.instance.pk:
            # If updating an existing spending, set the queryset based on the existing category
            self.initial['category'] = self.instance.category.pk
            self.fields['sub_category'].queryset = self.instance.category.subcategory_set.all()