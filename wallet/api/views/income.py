from rest_framework import generics, permissions
from wallet.models.income import Income
from wallet.api.serializers.income import IncomeSerializer


class IncomeListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def perform_create(self, serializer): # this logic authomatically puts logged user as the one who is creating expense
        serializer.save(member=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(member=user)


class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer