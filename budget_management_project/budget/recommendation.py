import datetime
import calendar
import math
from collections import defaultdict
from django.db.models import Sum
from budget_management_project.budget.models import Budget
from budget_management_project.expense.models import Expense, Category

def calculate_and_generate_budget_report(user, serializer):
    today = datetime.date.today()
    
    budget_objs = Budget.objects.filter(user=user, budget_date=today)
    if not budget_objs.exists():
        return None, "오늘의 예산 설정부터 해주세요!"
    
    total_budget = budget_objs.aggregate(total=sum('budget_amount'))['total'] or 0
    month_days = calendar.monthrange(today.year, today.month)[1]
    remaining_days = max(1, month_days - today.day)

    categories = Category.objects.all()
    category_names = {category.id: category.description for category in categories}
    
    daily_budget_message = (
        f"오늘 사용 가능한 금액은 총 {total_budget // remaining_days:,}원 이며,\n"
        "각 하루 사용 가능 금액:\n"
    )
    
    for budget in budget_objs:
        category_id = budget.category.id
        category_name = category_names.get(category_id, "알 수 없음")
        daily_category_budget = math.floor(budget.budget_amount / remaining_days)
        daily_budget_message += f"- {category_name}: {daily_category_budget:,}원\n"
    
    return None, daily_budget_message