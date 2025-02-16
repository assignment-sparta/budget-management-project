from rest_framework import serializers
from django.db.models import Sum

from budget_management_project.budget.models import Budget
from budget_management_project.expense.enums import CategoryType


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


class BudgetRecommendSerializer(serializers.Serializer):
    total_amount = serializers.IntegerField(min_value=0)
    
    class Meta:
        fields = ['total_amount']

    def create(self, validated_data):
        total_amount = validated_data['total_amount']
        recommendations = self.get_budget_recommendations(total_amount)
        return {'recommendations': recommendations}

    def get_budget_recommendations(self, total_amount):
        user_budgets = self.get_user_total_budgets()
        average_category_ratios = self.calculate_category_ratios(user_budgets)
        recommendations = self.generate_recommendations(average_category_ratios, total_amount)
        return recommendations


    def get_user_total_budgets(self):
        return Budget.objects.values('user').annotate(total_budget=Sum('budget_amount'))


    def calculate_category_ratios(self, user_budgets):
        user_category_ratios = {}  
        users_count = 0           
        category_averages = {} 

        for user_budget in user_budgets:
            users_count += 1
            user_id = user_budget['user']
            user_total = user_budget['total_budget']

            category_budgets = Budget.objects.filter(user=user_id)
            
            for budget in category_budgets:
                category = budget.category
                ratio = (budget.budget_amount / user_total) * 100

                if category not in user_category_ratios:
                    user_category_ratios[category] = 0
                user_category_ratios[category] += ratio

        if not users_count:
            raise serializers.ValidationError("추천을 위한 예산 데이터가 충분하지 않습니다.")

        for category, total_ratio in user_category_ratios.items():
            avg_ratio = round(total_ratio / users_count, 2)
            category_averages[category] = avg_ratio

        return category_averages

    def generate_recommendations(self, category_averages, total_amount):
        recommendations = []
        others_amount = 0
        others_ratio = 0

        for category, ratio in category_averages.items():
            if ratio >= 10:
                recommended_amount = int(total_amount * (ratio / 100))
                recommendations.append({
                    'category': category.id,
                    'category_name': category.description,
                    'ratio': ratio,
                    'amount': recommended_amount
                })
            else:
                others_ratio += ratio
                others_amount += int(total_amount * (ratio / 100))

        if others_amount > 0:
            recommendations.append({
                'category': CategoryType.ETC.value,
                'category_name': CategoryType.ETC.description,
                'ratio': round(others_ratio, 2),
                'amount': others_amount
            })

        return recommendations