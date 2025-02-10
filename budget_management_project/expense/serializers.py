from rest_framework import serializers
from .models import Category, Expense

class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['category', 'expense_money', 'expense_date', 'memo']
    
    def create(self, validated_data):
        # 현재 인증된 사용자를 지출 데이터에 추가
        user = self.context['request'].user
        expense = Expense.objects.create(
            user=user,
            **validated_data
        )
        return expense
    
class ExpenseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['category', 'expense_money', 'expense_date', 'memo']
    
    def validate(self, data):
        # 현재 사용자가 해당 지출의 소유자인지 확인
        expense = self.instance
        request = self.context.get('request')
        if expense.user != request.user:
            raise serializers.ValidationError("이 지출을 수정할 권한이 없습니다.")
        return data
    
    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.expense_money = validated_data.get('expense_money', instance.expense_money)
        instance.expense_date = validated_data.get('expense_date', instance.expense_date)
        instance.memo = validated_data.get('memo', instance.memo)
        instance.save()
        return instance