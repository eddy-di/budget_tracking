from rest_framework import serializers
from wallet.models.income import Income


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'amount', 'currency', 'comment', 'created_at', 'category', 'sub_category', 'wallet', 'member']
