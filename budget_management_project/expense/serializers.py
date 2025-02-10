from rest_framework import serializers
from expense.models import Category, Expense

class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['category', 'expense_money', 'expense_date', 'memo']
    
class ExpenseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['category', 'expense_money', 'expense_date', 'memo']

# 응답용 시리얼라이저 추가
class ExpenseResponseSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Expense
        fields = ['id', 'category', 'expense_money', 'expense_date', 'memo', 'created_at']