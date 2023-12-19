from rest_framework import serializers
from wallet.models.wallet import Wallet
from wallet.models.income import Income
from wallet.models.expense import Expense
from django.contrib.auth.models import User
from .income import IncomeSerializer
from .expense import ExpenseSerializer


class WalletListSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    # user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Wallet
        fields = ['id', 'name', 'slug', 'users']
    

class WalletDetailSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    # user = serializers.ReadOnlyField(source='user.username')
    incomes = serializers.SerializerMethodField()
    expenses = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ['id', 'name', 'slug', 'users', 'incomes', 'expenses']
    
    def get_incomes(self, obj):
        # obj represents the current instance of the Wallet model
        incomes = Income.objects.filter(wallet=obj)
        serializer = IncomeSerializer(incomes, many=True, context=self.context)
        return serializer.data
    
    def get_expenses(self, obj):
        # obj represents the current instance of the Wallet model
        expenses = Expense.objects.filter(wallet=obj)
        serializer = ExpenseSerializer(expenses, many=True, context=self.context)
        return serializer.data

