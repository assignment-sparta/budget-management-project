from datetime import date

from django.core.validators import MaxValueValidator
from rest_framework import serializers

from budget_management_project.expense.models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'type', 'description']


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.description', read_only=True)
    formatted_money = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    expense_money = serializers.IntegerField(min_value=1, write_only=True)
    expense_date = serializers.DateField(validators=[MaxValueValidator(limit_value=date.today)])

    class Meta:
        model = Expense
        fields = [
            'id',
            'user',
            'category',
            'category_name',
            'expense_money',
            'formatted_money',
            'expense_date',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'category_name',
            'formatted_money'
        ]

    def get_formatted_money(self, obj):
        return f"{obj.expense_money:,}원"