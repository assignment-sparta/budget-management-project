from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from budget_management_project.budget.models import Budget
from budget_management_project.budget.serializers import BudgetSerializer, BudgetRecommendSerializer


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
    lookup_url_kwarg = 'budget_id'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class BudgetRecommendView(generics.CreateAPIView):
    """
    예산 추천 View
    """
    serializer_class = BudgetRecommendSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.create(serializer.validated_data)
        return Response(result['recommendations']) 