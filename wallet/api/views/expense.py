from rest_framework import generics, permissions, serializers
from wallet.models.expense import Expense
from wallet.models.wallet import Wallet
from wallet.api.permissions import IsUserAssociatedWithWallet
from wallet.api.serializers.expense import ExpenseSerializer


class ExpenseListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        # Ensure required fields are provided in the request data
        required_fields = {'comment', 'category', 'sub_category'}
        request_data = self.request.data
        missing_fields = required_fields - set(request_data.keys())

        if missing_fields:
            raise serializers.ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Associate the new expense instance with the wallet and the current user
        wallet_id = self.request.data.get('wallet')
        wallet = Wallet.objects.get(pk=wallet_id)
        serializer.save(wallet=wallet, member=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(wallet__users=user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsUserAssociatedWithWallet]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer