from django.contrib.auth.models import User
from wallet.models.expense import Expense
from wallet.models.income import Income
from wallet.models.wallet import Wallet
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    wallet_expenses = serializers.PrimaryKeyRelatedField(many=True, queryset=Expense.objects.all())
    wallet_incomes = serializers.PrimaryKeyRelatedField(many=True, queryset=Income.objects.all())
    wallet_users = serializers.PrimaryKeyRelatedField(many=True, queryset=Wallet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'wallet_expenses', 'wallet_incomes', 'wallet_users']