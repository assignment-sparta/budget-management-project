from rest_framework import serializers
from budget.models import Budget
from budget_management_project.expense.models import Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'user', 'category', 'budget_money', 'budget_date', 'recommended_amount', 'risk_rate', 'created_at', 'updated_at']