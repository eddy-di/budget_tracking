from rest_framework import generics
from wallet.models.income import Income
from wallet.api.serializers.income import IncomeSerializer


class IncomeListView(generics.ListAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class IncomeDetailView(generics.RetrieveAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer