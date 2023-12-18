from rest_framework import generics, permissions
from wallet.models.income import Income
from wallet.models.wallet import Wallet
from wallet.api.permissions import IsUserAssociatedWithWallet
from wallet.api.serializers.income import IncomeSerializer


class IncomeListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def perform_create(self, serializer):
        # serializer.save(member=self.request.user)
        wallet_id = self.request.data.get('wallet')
        wallet = Wallet.objects.get(pk=wallet_id)
        serializer.save(wallet=wallet, member=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        # Show all instances of Income to users associated with the Wallet
        return Income.objects.filter(wallet__user=user) # member__wallet_users=user,


class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAssociatedWithWallet]
