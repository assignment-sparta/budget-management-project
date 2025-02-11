from django.utils import timezone
from rest_framework import serializers

from expense.models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    formatted_money = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

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
        read_only_fields = ['id', 'created_at']

    def validate_expense_money(self, value):
        if value <= 0:
            raise serializers.ValidationError("지출 금액은 0보다 커야 합니다.")
        return value
    
    def validate_expense_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("미래 날짜로 지출을 등록할 수 없습니다.")
        return value

    def get_formatted_money(self, obj):
        return f"{obj.expense_money:,}원"