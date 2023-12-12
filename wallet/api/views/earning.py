from rest_framework import generics
from wallet.models.income import Income
from wallet.api.serializers.earning import EarningSerializer


class EarningListView(generics.ListAPIView):
    queryset = Income.objects.all()
    serializer_class = EarningSerializer


class EarningDetailView(generics.RetrieveAPIView):
    queryset = Income.objects.all()
    serializer_class = EarningSerializer