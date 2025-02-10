from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import date
from .serializers import ExpenseCreateSerializer, ExpenseUpdateSerializer
import calendar
from rest_framework.decorators import api_view
from .models import Expense
from expense.enums import CategoryType


class ExpenseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ExpenseCreateSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            expense = serializer.save()
            return Response({
                'message': '지출이 성공적으로 생성되었습니다.',
                'data': {
                    'expense_id': expense.id,
                    'category': expense.category.name,
                    'expense_money': expense.expense_money,
                    'expense_date': expense.expense_date,
                    'memo': expense.memo,
                    'created_at': expense.created_at
                }
            }, status=status.HTTP_201_CREATED)


class ExpenseUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id)

        # 권한 확인
        if expense.user != request.user:
            return Response({
                "message": "이 지출을 수정할 권한이 없습니다."
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = ExpenseUpdateSerializer(
            expense,
            data=request.data,
            context={'request': request},
            partial=True  # 부분 업데이트 허용
        )

        if serializer.is_valid():
            updated_expense = serializer.save()
            return Response({
                'message': '지출이 성공적으로 수정되었습니다.',
                'data': {
                    'expense_id': updated_expense.id,
                    'category': updated_expense.category.name,
                    'expense_money': updated_expense.expense_money,
                    'expense_date': updated_expense.expense_date,
                    'memo': updated_expense.memo,
                    'updated_at': updated_expense.updated_at
                }
            }, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )