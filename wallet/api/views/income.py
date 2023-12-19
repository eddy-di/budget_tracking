from rest_framework import generics, permissions, serializers
from wallet.models.income import Income
from wallet.models.wallet import Wallet
from wallet.api.permissions import IsUserAssociatedWithWallet
from wallet.api.serializers.income import IncomeSerializer


class IncomeListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def perform_create(self, serializer):
        # Ensure required fields are provided in the request data
        required_fields = {'comment', 'category', 'sub_category'}
        request_data = self.request.data
        missing_fields = required_fields - set(request_data.keys())

        if missing_fields:
            raise serializers.ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

        wallet_id = self.request.data.get('wallet')
        wallet = Wallet.objects.get(pk=wallet_id)
        serializer.save(wallet=wallet, member=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        # Show all instances of Income to users associated with the Wallet
        return Income.objects.filter(wallet__users=user) # member__wallet_users=user,


class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAssociatedWithWallet]
