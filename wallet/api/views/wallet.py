from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from wallet.models.wallet import Wallet
from wallet.api.serializers.wallet import WalletSerializer


class WalletListCreateView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer): # this logic authomatically puts logged user as the one who is creating expense
        serializer.save(user=[self.request.user])

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(user=user)


class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(user=user)