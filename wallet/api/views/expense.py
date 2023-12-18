from rest_framework import generics, permissions
from wallet.models.expense import Expense
from wallet.models.wallet import Wallet
from wallet.api.permissions import IsUserAssociatedWithWallet
from wallet.api.serializers.expense import ExpenseSerializer


class ExpenseListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer): # this logic authomatically puts logged user as the one who is creating expense
        # Associate the new expense instance with the wallet and the current user
        wallet_id = self.request.data.get('wallet')
        wallet = Wallet.objects.get(pk=wallet_id)
        serializer.save(wallet=wallet, member=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(wallet__user=user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsUserAssociatedWithWallet]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer