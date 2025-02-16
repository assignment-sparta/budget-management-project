from datetime import date

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


class LastMonthComparisonSerializer(serializers.Serializer):
    category = serializers.CharField(source='category__description')
    percentage = serializers.IntegerField()


class LastWeekdayComparisonSerializer(serializers.Serializer):
    weekday = serializers.CharField()
    comparison_rate = serializers.IntegerField()


class OtherUsersComparisonSerializer(serializers.Serializer):
    other_users_rate = serializers.FloatField()
    my_usage_rate = serializers.FloatField()
    average_usage_rate = serializers.FloatField()


class ExpenseStatisticsSerializer(serializers.Serializer):
    last_month_comparison = LastMonthComparisonSerializer(many=True)
    last_weekday_comparison = LastWeekdayComparisonSerializer()
    other_users_comparison = OtherUsersComparisonSerializer()