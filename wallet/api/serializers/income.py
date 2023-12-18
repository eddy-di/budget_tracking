from rest_framework import serializers
from wallet.models.income import Income
from wallet.models.wallet import Wallet
from wallet.models.category import Category
from wallet.models.sub_category import SubCategory

from decimal import Decimal
from django.core.validators import MinValueValidator



class IncomeSerializer(serializers.ModelSerializer):
    wallet = serializers.PrimaryKeyRelatedField(many=False, queryset=Wallet.objects.all())
    member = serializers.ReadOnlyField(source='member.username') # this part doesn't show up when user is saving expense

    amount = serializers.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal('0.00'))],
        required=True
    )
    comment = serializers.CharField(
        allow_blank=True,
        required=False
    )
    currency = serializers.ChoiceField(
        choices=Income.CurrencyChoices.choices,
        default=Income.CurrencyChoices.KGS,
        # required=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
    )
    sub_category = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(),
        required=True
    )


    class Meta:
        model = Income
        fields = [
            'id', 
            'amount', 
            'currency', 
            'comment', 
            'created_at', 
            'category', 
            'sub_category', 
            'wallet', 
            'member'
                  ]
