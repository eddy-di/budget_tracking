from rest_framework import serializers
from wallet.models.wallet import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'slug', 'user']