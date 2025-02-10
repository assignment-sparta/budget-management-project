from rest_framework import serializers
from .models import Budget
from budget_management_project.expense.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        model = Category
        fields = '__all__'
        

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'