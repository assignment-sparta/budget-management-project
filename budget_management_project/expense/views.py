# Django 관련 임포트
from django.shortcuts import get_object_or_404

# DRF 관련 임포트
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# 로컬 애플리케이션
from expense.models import Expense
from expense.serializers import ExpenseCreateSerializer, ExpenseUpdateSerializer, ExpenseResponseSerializer
from expense.permissions import IsExpenseOwner

class ExpenseCreateView(generics.CreateAPIView):
    serializer_class = ExpenseCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        expense = Expense.objects.get(id=response.data['id'])
        response_serializer = ExpenseResponseSerializer(expense)

        return Response({
            'message': '지출이 성공적으로 생성되었습니다.',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)

class ExpenseUpdateView(generics.UpdateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseUpdateSerializer
    permission_classes = [IsAuthenticated, IsExpenseOwner]
    lookup_url_kwarg = 'expense_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_serializer = ExpenseResponseSerializer(instance)
        return Response({
            'message': '지출이 성공적으로 수정되었습니다.',
            'data': response_serializer.data
        })