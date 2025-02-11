from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from expense.serializers import ExpenseSerializer
from expense.permissions import IsExpenseOwner

class ExpenseCreateView(generics.CreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsExpenseOwner]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': '지출이 성공적으로 생성되었습니다.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class ExpenseUpdateView(generics.UpdateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsExpenseOwner]
    
    from urllib import request #예시임 나중에 삭제
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import date
import calendar
from .models import Expense
from expense.enums import CategoryType
from budget.models import Budget, Expense
from .models import Expense
# Create your views here.

today = date.today()
budget_db = get_object_or_404(Budget, user = request.user)
expense_db = get_object_or_404(Expense, user = request.user, expense_date = today)
if budget_db.total_amount:
    #------------------------------------------------------------
    # Budget
    budget_obj = Budget.objects.order_by('-id').first()
    budget_amount = budget_obj.amount
    budget_category = budget_obj.category
    # 날짜
    partial_date = budget_obj.budget_date
    #------------------------------------------------------------
    # Expense
    expense_category = expense_db.category
    expense_daily = expense_db.expense_money
    # 날짜
    expense_date = expense_db.expense_date
    #------------------------------------------------------------
    month_days = calendar.monthrange(today.year, today.month)[1]
    remaining_days = max(1, month_days-today.day)
    budget_daily_available = round(budget_amount/remaining_days)
    daily_available = budget_db.total_amount // remaining_days
    #------------------------------------------------------------
    # Budget
    category_ids= [
        category.code for category in CategoryType
    ]
    category_name = [
        category.name for category in CategoryType
    ]
    #------------------------------------------------------------
    #budget
    choosen_category_budget = category_ids[budget_category - 1]
    choosen_category_budget_name = category_name[choosen_category_budget]
    #------------------------------------------------------------
    # Expense
    choosen_category_expense = category_ids[expense_category - 1]
    choosen_category_expense_name = category_name[choosen_category_expense]
    response = {'meesages': f"오늘 사용가능 한 금액은 {daily_available}이며, 현재 알려주신 정보를 토대로 {choosen_category_budget_name}의 하루 사용 가능 금액은 {budget_daily_available}입니다."}
    
#---------------------------------------------------------------------------
    expense_category = expense_db.category
    expense_daily = expense_db.expense_money
    expense_date = expense_db.expense_date
    if budget_daily_available > expense_daily:
        remain_percentage = ((budget_daily_available - expense_daily) / budget_daily_available) * 100
        budget_db.total_amount -= expense_daily
        budget_amount -= expense_daily
        budget_db.save()
        budget_obj.save()
        remain_response = {"messages" : f"{choosen_category_budget_name}의 절약을 잘 실천하셨네요! 오늘도 절약 도전! 오늘 절약률은 {remain_percentage}입니다!"}
    else:
        excessive_precentage = ((expense_daily - budget_daily_available) / budget_daily_available) * 100
        budget_db.total_amount -= expense_daily
        budget_amount -= expense_daily
        budget_db.save()
        budget_obj.save()
        excessive_response = {"messages" : f"이런..{choosen_category_expense_name}하루 예산 이상을 쓰셨군요.. 괜찮아요! 더 절약하죠! 오늘 지출은 사용가능의 {excessive_precentage}입니다!"}