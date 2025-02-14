from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from budget_management_project.expense.models import Category, Expense
from budget_management_project.expense.serializers import CategorySerializer, ExpenseSerializer
from budget_management_project.expense.permissions import IsExpenseOwner
from budget_management_project.expense.enums import CategoryType

class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        for category_type in CategoryType:
            Category.objects.get_or_create(type=category_type.code)
        return super().get_queryset()


class BaseExpenseView(generics.GenericAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsExpenseOwner]
    lookup_url_kwarg = 'expense_id'

    def get_queryset(self):
        return Expense.objects.all()


class ExpenseCreateView(BaseExpenseView, generics.ListCreateAPIView):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': '지출 목록 조회 성공',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': '지출이 성공적으로 생성되었습니다.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class ExpenseDetailView(BaseExpenseView, generics.RetrieveUpdateDestroyAPIView):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': '지출 상세 조회 성공',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': '지출이 성공적으로 수정되었습니다.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'message': '지출이 성공적으로 삭제되었습니다.'
        }, status=status.HTTP_204_NO_CONTENT)


class ExpenseExcludeView(BaseExpenseView, generics.UpdateAPIView):
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_excluded = not instance.is_excluded
        instance.save()
        
        message = '지출이 합계에서 제외되었습니다.' if instance.is_excluded else '지출이 합계에 포함되었습니다.'
        return Response({
            'message': message,
            'data': self.get_serializer(instance).data
        }, status=status.HTTP_200_OK)
