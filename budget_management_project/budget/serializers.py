from rest_framework import serializers
from budget_management_project.budget.models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    """
    예산 시리얼라이저
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Budget
        fields = ['id','user','category','category_name','budget_amount','budget_date']