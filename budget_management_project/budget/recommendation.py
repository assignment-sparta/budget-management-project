import datetime
import calendar
import math
from collections import defaultdict
from django.db.models import Sum
from budget_management_project.budget.models import Budget
from budget_management_project.expense.models import Expense, Category
import time

def calculate_and_generate_budget_report(user):
    today = datetime.date.today()

    latest_budget = Budget.objects.filter(user=user, budget_date=today).order_by('-id').first()
    if not latest_budget:
        return None, "오늘의 예산 설정부터 해주세요!"

    total_budget = latest_budget.budget_amount
    month_days = calendar.monthrange(today.year, today.month)[1]
    remaining_days = max(1, month_days - today.day)

    category_name = latest_budget.category.description if latest_budget.category else "알 수 없음"
    daily_category_budget = math.floor(total_budget / remaining_days)

    daily_budget_message = (
        f"오늘 사용 가능한 금액은 총 {total_budget // remaining_days:,}원 이며,\n"
        "각 하루 사용 가능 금액:\n"
        f"- {category_name}: {daily_category_budget:,}원\n"
    )

    return None, daily_budget_message