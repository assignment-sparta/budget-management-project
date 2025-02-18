from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from django.db import transaction

from budget_management_project.budget.models import Budget
from budget_management_project.budget.serializers import BudgetSerializer, BudgetRecommendSerializer
from budget_management_project.budget.recommendation import calculate_and_generate_budget_report

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        budget_instance = serializer.save(user=request.user)
        
        budget_instance.refresh_from_db()

        _, message = calculate_and_generate_budget_report(request.user)
        return Response(
            {"message": message or "예산 등록 완료!", "data": serializer.data}
        )
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