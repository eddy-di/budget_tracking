from rest_framework import generics
from wallet.models.wallet import Wallet
from wallet.api.serializers.wallet import WalletSerializer


class WalletListView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletDetailView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer