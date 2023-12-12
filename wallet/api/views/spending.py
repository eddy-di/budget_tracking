from rest_framework import generics
from wallet.models.spending import Spending
from wallet.api.serializers.spending import SpendingSerializer


class SpendingListView(generics.ListAPIView):
    queryset = Spending.objects.all()
    serializer_class = SpendingSerializer


class SpendingDetailView(generics.RetrieveAPIView):
    queryset = Spending.objects.all()
    serializer_class = SpendingSerializer