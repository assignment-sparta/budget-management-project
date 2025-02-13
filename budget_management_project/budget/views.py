from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from budget_management_project.budget.models import Budget
from budget_management_project.budget.serializers import BudgetSerializer


class BudgetView(generics.ListCreateAPIView):
    """
    예산 목록 조회 및 생성 View
    """
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    
class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    예산 수정, 삭제 View
    """
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)