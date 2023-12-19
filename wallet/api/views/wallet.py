from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from wallet.models.wallet import Wallet
from wallet.api.serializers.wallet import WalletListSerializer, WalletDetailSerializer
from wallet.api.permissions import IsUserAssociatedWithWalletDetail


class WalletListCreateView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=[self.request.user])

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(users=user)


class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsUserAssociatedWithWalletDetail]
    queryset = Wallet.objects.all()
    serializer_class = WalletDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(users=user)