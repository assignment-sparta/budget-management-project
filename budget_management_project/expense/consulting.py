from datetime import datetime
import calendar
from collections import defaultdict
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F
from django.db.models import Sum


from budget_management_project.budget.models import Budget
from budget_management_project.expense.models import Expense, Category



def calculate_and_generate_budget_report(user, serializer, today=None):
    created_at = serializer.validated_data.get('expense_date')
    if today is None:
        today = created_at or datetime.today().date()

    # Budget 쿼리셋 재설정
    budget_objs = Budget.objects.filter(user=user, category = serializer.validated_data["category"], budget_date=today)
    if not budget_objs.exists():
        return None, "이 카데고리에 대해 오늘의 예산 설정부터 해주세요!", ""

    # Expense 쿼리셋 재설정
    expense_objs = Expense.objects.filter(user=user, expense_date=created_at)
    expense_obj_check = Expense.objects.filter(user=user, category = serializer.validated_data["category"], expense_date=created_at)
    if expense_obj_check.exists():
        return None, "오늘은 이미 해당 카테고리에 대한 지출을 입력했습니다! 수정이나 다른 카테고리에 대한 값을 넣어주세요.", ""

    budget_data = defaultdict(int)
    expense_data = defaultdict(int)
    initial_budgets = {b.category.type: b.budget_amount for b in budget_objs}
    
    category_names = {c.type: c.description for c in Category.objects.all()}
    
    for budget in budget_objs:
        budget_data[budget.category.type] = budget.budget_amount
    
    for expense in expense_objs:
        expense_data[expense.category.type] += expense.expense_money

    month_days = calendar.monthrange(today.year, today.month)[1]
    remaining_days = max(1, month_days - today.day)
    
    update_response, remain_responses, excessive_responses, warnings = "", "", "", ""

    for category_id, category_budget in budget_data.items():
        category_name = category_names.get(category_id, "미등록 카테고리")
        daily_budget = round(category_budget / remaining_days)
        daily_expense = expense_data.get(category_id, 0)

        budget = budget_objs.filter(category__type=category_id).first()
        if budget:
            budget.budget_amount -= daily_expense
            budget.save()
        
        if daily_budget > daily_expense:
            remain_percentage = ((daily_budget - daily_expense) / daily_budget) * 100
            remain_responses += f"오늘 {daily_expense}원을 쓰셨군요! {category_name} 절약률: {remain_percentage:.2f}%\n"
        else:
            excessive_percentage = ((daily_expense - daily_budget) / daily_budget) * 100
            excessive_responses += f"오늘 {daily_expense}원을 쓰셨군요! {category_name} 과소비율: {excessive_percentage:.2f}%\n"

        initial_budget = initial_budgets.get(category_id, 0)
        if initial_budget and budget.budget_amount < initial_budget * 0.2:
            warnings += f"{category_name} 예산이 위험 수준이에요!\n"
        else:
            warnings += f"{category_name} 예산이 적당한 수준에 있어요!\n"
    serializer.save()
    return remain_responses, excessive_responses, warnings




def calculate_and_generate_updated_budget_report(user, serializer, today=None):
    created_at = serializer.validated_data.get('expense_date')
    if today is None:
        today = created_at or datetime.today().date()

    budget_objs = Budget.objects.filter(user=user, budget_date=today)
    if not budget_objs.exists():
        return None, "오늘의 예산 설정부터 해주세요!", ""

    expense_objs = Expense.objects.filter(user=user, expense_date=created_at)
    old_amount = expense_objs.filter(category=serializer.validated_data['category']).aggregate(Sum('expense_money'))['expense_money__sum'] or 0

    serializer.save()
    new_amount = serializer.validated_data['expense_money']
    category = serializer.validated_data['category']
    
    # 차액만 반영
    diff = new_amount - old_amount
    Budget.objects.filter(user=user, category=category, budget_date=today).update(
        budget_amount=F('budget_amount') - diff
    )

    budget_data = {b.category.type: b.budget_amount for b in budget_objs}
    initial_budgets = budget_data.copy()
    category_names = {c.type: c.description for c in Category.objects.all()}

    month_days = calendar.monthrange(today.year, today.month)[1]
    remaining_days = max(1, month_days - today.day)

    update_excessive_reponse, remain_responses, excessive_responses, warnings = "", "", "", ""
    
    for category_id, category_budget in budget_data.items():
        category_name = category_names.get(category_id, "미등록 카테고리")
        daily_budget = round(category_budget / remaining_days)
        daily_expense = new_amount if category_id == category.type else 0

        if daily_budget > daily_expense:
            remain_percentage = ((daily_budget - daily_expense) / daily_budget) * 100
            remain_responses += f"오늘 수정된 {daily_expense}원을 쓰셨군요! {category_name} 절약률: {remain_percentage:.2f}%\n"
        else:
            excessive_percentage = ((daily_expense - daily_budget) / daily_budget) * 100
            excessive_responses += f"오늘 수정된 {daily_expense}원을 쓰셨군요! {category_name} 과소비율: {excessive_percentage:.2f}%\n"

        initial_budget = initial_budgets.get(category_id, 0)
        if initial_budget and category_budget < initial_budget * 0.2:
            warnings += f"{category_name} 예산이 수정된 값에서 위험 수준이에요!\n"
        else:
            warnings += f"{category_name} 예산이 수정된 값에서 적당한 수준에 있어요!\n"

    return remain_responses, excessive_responses, warnings
