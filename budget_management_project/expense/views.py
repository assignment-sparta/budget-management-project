from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from budget_management_project.expense.models import Category, Expense
from budget_management_project.budget.serializers import CategorySerializer
from budget_management_project.expense.serializers import ExpenseSerializer
from budget_management_project.expense.permissions import IsExpenseOwner


class CategoryView(APIView):
    '''
    카테고리 관련 APIView
    '''
    permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({
            "message": "카테고리 목록 조회 성공",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class BaseExpenseView(generics.GenericAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsExpenseOwner]
    lookup_url_kwarg = 'expense_id'

    def get_queryset(self):
        return Expense.objects.all()

class ExpenseCreateView(BaseExpenseView, generics.CreateAPIView):
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': '지출이 성공적으로 생성되었습니다.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class ExpenseUpdateView(BaseExpenseView, generics.UpdateAPIView):
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': '지출이 성공적으로 수정되었습니다.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class ExpenseDeleteView(BaseExpenseView, generics.DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'message': '지출이 성공적으로 삭제되었습니다.'
        }, status=status.HTTP_204_NO_CONTENT)

class ExpenseListView(BaseExpenseView, generics.ListAPIView):
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(user=user)
        
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        try:
            if start_date and end_date:
                filters = {
                    'expense_date__range': [start_date, end_date]
                }
                
                if category := self.request.query_params.get('category'):
                    filters['category_id'] = category
                    
                if min_amount := self.request.query_params.get('min_amount'):
                    filters['expense_money__gte'] = min_amount
                if max_amount := self.request.query_params.get('max_amount'):
                    filters['expense_money__lte'] = max_amount
                    
                return queryset.filter(**filters)
            else:
                raise ValidationError("start_date와 end_date는 필수 파라미터입니다.")
        except ValueError:
            raise ValidationError("날짜 형식이 올바르지 않습니다.")
    
class ExpenseDetailView(BaseExpenseView, generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': '지출 상세 조회 성공',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class ExpenseExcludeView(BaseExpenseView, generics.UpdateAPIView):
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_excluded = not instance.is_excluded
        instance.save()
        
        message = '지출이 합계에서 제외되었습니다.' if instance.is_excluded else '지출이 합계에 포함되었습니다.'
        return Response({
            'message': message,
            'data': self.get_serializer(instance).data
        }, status=status.HTTP_200_OK)
