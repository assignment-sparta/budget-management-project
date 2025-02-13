from django.utils import timezone
from django.utils.timezone import now
from django.core.validators import MaxValueValidator
from rest_framework import serializers
from budget_management_project.expense.models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'type', 'description']


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    formatted_money = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    expense_money = serializers.IntegerField(min_value=1)
    expense_date = serializers.DateTimeField(validators=[MaxValueValidator(limit_value=now)])

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
            'memo',
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