from rest_framework import serializers
from wallet.models.expense import Expense
from wallet.models.wallet import Wallet


class ExpenseSerializer(serializers.ModelSerializer):
    wallet = serializers.PrimaryKeyRelatedField(many=False, queryset=Wallet.objects.all())
    member = serializers.ReadOnlyField(source='member.username') # this part doesn't show up when user is saving expense

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'currency', 'comment', 'created_at', 'category', 'sub_category', 'wallet', 'member']