from rest_framework import serializers
from wallet.models.expense import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'currency', 'comment', 'created_at', 'category', 'sub_category', 'wallet', 'member']