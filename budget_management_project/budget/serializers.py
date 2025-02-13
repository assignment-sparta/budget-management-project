from rest_framework import serializers
from budget_management_project.budget.models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'user', 'category', 'budget_money', 'budget_date', 'recommended_amount', 'risk_rate', 'created_at', 'updated_at']