from django import forms
from .models.comment_expense import ExpenseComment, Expense
from .models.comment_income import IncomeComment, Income
from .models.wallet import Wallet
from .models.sub_category import SubCategory
from .models.category import Category
from .models.invite import Invite


class EmailExpenseForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class ExpenseCommentForm(forms.ModelForm):
    class Meta:
        model = ExpenseComment
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


class ExpenseAddForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), 
                                      widget=forms.Select(attrs={'hx-get': 'get_subcategories/', 
                                                                 'hx-target': '#id_sub_category'}))
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.none())

    class Meta:
        model = Expense
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
            # If updating an existing expense, set the queryset based on the existing category
            self.initial['category'] = self.instance.category.pk
            self.fields['sub_category'].queryset = self.instance.category.subcategory_set.all()



class IncomeAddForm(forms.ModelForm):
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
            # If updating an existing expense, set the queryset based on the existing category
            self.initial['category'] = self.instance.category.pk
            self.fields['sub_category'].queryset = self.instance.category.subcategory_set.all()


class InviteForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    wallet = forms.ModelChoiceField(queryset=Wallet.objects.none(), label='Your wallets')

    class Meta:
        model = Invite
        exclude = ['token', 'expiration_date', 'user', 'is_deleted']
        fields = ['wallet', 'email']

    def __init__(self, user, *args, **kwargs):
        super(InviteForm, self).__init__(*args, **kwargs)
        wallets = Wallet.objects.filter(users=user)
        self.fields['wallet'].queryset = wallets