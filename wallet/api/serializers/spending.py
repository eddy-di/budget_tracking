from rest_framework import serializers
from wallet.models.spending import Spending

class SpendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spending
        fields = ['id', 'amount', 'currency', 'comment', 'created_at', 'category', 'sub_category', 'wallet', 'member']