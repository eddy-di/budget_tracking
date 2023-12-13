from rest_framework import generics
from wallet.models.expense import Expense
from wallet.api.serializers.expense import ExpenseSerializer


class ExpenseListView(generics.ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class ExpenseDetailView(generics.RetrieveAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer