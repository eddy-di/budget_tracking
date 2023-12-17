from rest_framework import serializers
from wallet.models.wallet import Wallet
from django.contrib.auth.models import User


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    # user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Wallet
        fields = ['id', 'name', 'slug', 'user']

