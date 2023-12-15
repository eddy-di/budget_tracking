from rest_framework import generics, permissions
from wallet.models.expense import Expense
from wallet.api.serializers.expense import ExpenseSerializer


class ExpenseListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer): # this logic authomatically puts logged user as the one who is creating expense
        serializer.save(member=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer