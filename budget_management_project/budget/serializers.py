from rest_framework import serializers
from budget_management_project.budget.models import Budget



class BudgetSerializer(serializers.ModelSerializer):
    """
    예산 시리얼라이저
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_name = serializers.CharField(source='category.description', read_only=True)
    budget_amount = serializers.IntegerField(write_only=True)
    formatted_money = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = ['id','user','category','category_name','budget_amount','formatted_money','budget_date']
    
    def get_formatted_money(self, obj):
        return f"{obj.budget_amount:,}원"