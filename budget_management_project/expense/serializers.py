from rest_framework import serializers
from .models import Category, Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['category', 'expense_money', 'expense_date', 'created_at']