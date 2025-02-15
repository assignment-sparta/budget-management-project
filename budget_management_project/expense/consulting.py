import datetime
import calendar
from collections import defaultdict
from budget_management_project.budget.models import Budget
from budget_management_project.expense.models import Expense, Category
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F

def calculate_and_generate_budget_report(user, serializer, today=None):
    if today is None:
        today = datetime.date.today()

    budget_objs = Budget.objects.filter(user=user, budget_date=today)
    expense_objs = Expense.objects.filter(user=user, expense_date=today)
    if not budget_objs.exists():
        return None, "오늘의 예산 설정부터 해주세요!"

    budget_data = defaultdict(int)
    expense_data = defaultdict(int)
    budget_initial_values = {}

    for budget in budget_objs:
        category_id = budget.category.type
        budget_data[category_id] += budget.budget_amount
        budget_initial_values[category_id] = budget.budget_amount

    for expense in expense_objs:
        category_id = expense.category.type
        expense_data[category_id] += expense.expense_money

    month_days = calendar.monthrange(today.year, today.month)[1]
    remaining_days = max(1, month_days - today.day)

    category_names = {category.type: category.description for category in Category.objects.all()}

    daily_budget_message = "오늘 사용 가능한 금액은 총 {}원 이며,\n".format(sum(budget_data.values()) // remaining_days)
    daily_budget_message += "각 하루 사용 가능 금액:\n"
    remain_responses = ""
    excessive_responses = ""
    warnings = ""

    for category_id, category_budget in budget_data.items():
        category_name = category_names.get(category_id, "이 목록은 아직 값이 들어가지 않았어요! 먼저 예산 설정부터 부탁드립니다!")
        daily_category_budget = round(category_budget / remaining_days)
        daily_category_expense = expense_data.get(category_id, 0)

        daily_budget_message += f"- {category_name}: {daily_category_budget}원\n"
        budget_data[category_id] -= daily_category_expense
        budget.budget_amount = budget_data[category_id] - daily_category_expense
        budget.save()
        if daily_category_budget > daily_category_expense:
            remain_percentage = ((daily_category_budget - daily_category_expense) / daily_category_budget) * 100
            remain_responses += f"{category_name} 절약을 잘 하셨어요! 절약률: {remain_percentage:.2f}%\n"
        else:
            excessive_percentage = ((daily_category_expense - daily_category_budget) / daily_category_budget) * 100
            excessive_responses += f"{category_name} 과소비 했어요! 과소비율: {excessive_percentage:.2f}%\n"

        initial_budget = budget_initial_values.get(category_id, 0)
        if initial_budget > 0 and category_budget < (initial_budget * 0.2):
            warnings += f"{category_name} 예산이 위험 수준이에요!\n"
        else:
            warnings += f"{category_name} 예산이 적당한 수준에 있어요!\n"

        return Response({
            'message': '지출이 성공적으로 생성되었습니다.',
            'data': serializer.data,
            'budget_report': {
                'daily_budget_message': daily_budget_message,
                'remain_responses': remain_responses,
                'excessive_responses': excessive_responses,
                'warnings': warnings,
            }
        }, status=status.HTTP_201_CREATED)


def calculate_and_generate_new_budget_report(user, serializer, today=None):
    expense_objs = Expense.objects.filter(user=user, expense_date=today)
    old_amount = sum(expense_objs.values_list('expense_money', flat=True))  
    old_categories = expense_objs.values_list('category', flat=True) 
    
    serializer.save()
    new_amount = serializer.validated_data['expense_money']
    new_category = serializer.validated_data['category']

    for old_category in set(old_categories):
        Budget.objects.filter(user=user, category=old_category, budget_date=today).update(
            budget_amount=F('budget_amount') - old_amount
        )

    Budget.objects.filter(user=user, category=new_category, budget_date=today).update(
        budget_amount=F('budget_amount') + new_amount
    )

    budget_objs = Budget.objects.filter(user=user, budget_date=today)
    expense_objs = Expense.objects.filter(user=user, expense_date=today)
    if not budget_objs.exists():
        return None, "오늘의 예산 설정부터 해주세요!"

    budget_data = defaultdict(int)
    expense_data = defaultdict(int)
    budget_initial_values = {}

    for budget in budget_objs:
        category_id = budget.category.type
        budget_data[category_id] += budget.budget_amount
        budget_initial_values[category_id] = budget.budget_amount

    for expense in expense_objs:
        category_id = expense.category.type
        expense_data[category_id] += expense.expense_money

    month_days = calendar.monthrange(today.year, today.month)[1]
    remaining_days = max(1, month_days - today.day)

    category_names = {category.type: category.description for category in Category.objects.all()}
    daily_budget_message = "오늘 사용 가능한 수정된 금액은 총 {}원 이며,\n".format(sum(budget_data.values()) // remaining_days)
    daily_budget_message += "각 수정된 하루 사용 가능 금액:\n"
    remain_responses = ""
    excessive_responses = ""
    warnings = ""

    for category_id, category_budget in budget_data.items():
        category_name = category_names.get(category_id, "이 목록은 아직 값이 들어가지 않았어요! 먼저 예산 설정부터 부탁드립니다!")
        daily_category_budget = round(category_budget / remaining_days)
        daily_category_expense = expense_data.get(category_id, 0)

        daily_budget_message += f"- {category_name}: {daily_category_budget}원\n"
        budget_data[category_id] -= daily_category_expense

        budget = Budget.objects.get(user=user, category_id=category_id, budget_date=today)
        budget.budget_amount = budget_data[category_id] - daily_category_expense
        budget.save()
        
        if daily_category_budget > daily_category_expense:
            remain_percentage = ((daily_category_budget - daily_category_expense) / daily_category_budget) * 100
            remain_responses += f"오늘 수정된 돈을 보니 {category_name} 절약을 잘 하셨어요! 절약률: {remain_percentage:.2f}%\n"
        else:
            excessive_percentage = ((daily_category_expense - daily_category_budget) / daily_category_budget) * 100
            excessive_responses += f"오늘 수정된 돈을 보니 {category_name} 과소비 했어요! 과소비율: {excessive_percentage:.2f}%\n"

        initial_budget = budget_initial_values.get(category_id, 0)
        if initial_budget > 0 and category_budget < (initial_budget * 0.2):
            warnings += f"수정된 값에서 {category_name} 예산이 위험 수준이에요!\n"
        else:
            warnings += f"수정된 값에서 {category_name} 예산이 적당한 수준에 있어요!\n"

    return Response({
        'message': '지출이 성공적으로 수정되었습니다.',
        'data': serializer.data,
        'budget_report': {
            'daily_budget_message': daily_budget_message,
            'remain_responses': remain_responses,
            'excessive_responses': excessive_responses,
            'warnings': warnings,
        }
    }, status=status.HTTP_200_OK)