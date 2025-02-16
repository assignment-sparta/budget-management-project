from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db import transaction, models
from django.db.models import Sum
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from budget_management_project.expense.models import Category, Expense
from budget_management_project.expense.serializers import CategorySerializer, ExpenseSerializer, ExpenseStatisticsSerializer
from budget_management_project.expense.permissions import IsExpenseOwner
from budget_management_project.expense.enums import CategoryType

class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        for category_type in CategoryType:
            Category.objects.get_or_create(type=category_type.code, description=category_type.description)
        return super().get_queryset()


class BaseExpenseView(generics.GenericAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsExpenseOwner]
    lookup_url_kwarg = 'expense_id'

    def get_queryset(self):
        return Expense.objects.all()


class ExpenseCreateView(BaseExpenseView, generics.ListCreateAPIView):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': '지출 목록 조회 성공',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        today = datetime.date.today()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        calculate_and_generate_budget_report(user, serializer, today)

class ExpenseDetailView(BaseExpenseView, generics.RetrieveUpdateDestroyAPIView):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': '지출 상세 조회 성공',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        today = datetime.date.today()
        user = request.user
        calculate_and_generate_new_budget_report(user, today)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'message': '지출이 성공적으로 삭제되었습니다.'
        }, status=status.HTTP_204_NO_CONTENT)


class ExpenseExcludeView(BaseExpenseView, generics.UpdateAPIView):
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_excluded = not instance.is_excluded
        instance.save()
        
        message = '지출이 합계에서 제외되었습니다.' if instance.is_excluded else '지출이 합계에 포함되었습니다.'
        return Response({
            'message': message,
            'data': self.get_serializer(instance).data
        }, status=status.HTTP_200_OK)
    

class ExpenseStatisticsView(APIView):
    """
    지출 통계 View
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        
        last_month_comparison = self._get_last_month_comparison(request.user, today)
        last_weekday_comparison = self._get_last_weekday_comparison(request.user, today)
        other_users_comparison = self._get_other_users_comparison(request.user, today)

        statistics_data = {
            'last_month_comparison': [
                {'category__description': category, 'percentage': value}
                for category, value in last_month_comparison.items()
            ],
            'last_weekday_comparison': last_weekday_comparison,
            'other_users_comparison': other_users_comparison
        }
        
        serializer = ExpenseStatisticsSerializer(data=statistics_data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _get_last_month_comparison(self, user, today):
        last_month_date = today - relativedelta(months=1)
        
        current_month_expenses = Expense.objects.filter(
            user=user,
            expense_date__year=today.year,
            expense_date__month=today.month,
            expense_date__day__lte=today.day,
            is_excluded=False
        ).values('category__description').annotate(
            total=Sum('expense_money')
        )
        
        last_month_expenses = Expense.objects.filter(
            user=user,
            expense_date__year=last_month_date.year,
            expense_date__month=last_month_date.month,
            expense_date__day__lte=last_month_date.day,
            is_excluded=False
        ).values('category__description').annotate(
            total=Sum('expense_money')
        )
        
        comparison_result = {}
        
        last_month_dict = {
            item['category__description']: item['total'] 
            for item in last_month_expenses
        }
        
        for current in current_month_expenses:
            category = current['category__description']
            current_amount = current['total']
            last_amount = last_month_dict.get(category, 0)
            
            if last_amount == 0:
                comparison_result[category] = 100 if current_amount > 0 else 0
            else:
                percentage = round((current_amount / last_amount) * 100)
                comparison_result[category] = percentage
        
        return comparison_result

    def _get_last_weekday_comparison(self, user, today):
        weekday_mapping = {
            0: '월요일',
            1: '화요일',
            2: '수요일',
            3: '목요일',
            4: '금요일',
            5: '토요일',
            6: '일요일'
        }
        

        current_weekday = today.weekday()
        weekday_name = weekday_mapping[current_weekday]
        

        today_expense = Expense.objects.filter(
            user=user,
            expense_date=today,
            is_excluded=False
        ).aggregate(total=Sum('expense_money'))['total'] or 0
        
        past_dates = [
            today - timedelta(days=(7 * week))
            for week in range(1, 5)
        ]

        past_weekday_expenses = Expense.objects.filter(
            user=user,
            expense_date__in=past_dates,
            is_excluded=False
        ).values('expense_date').annotate(
            daily_total=Sum('expense_money')
        )
        
        past_totals = [expense['daily_total'] for expense in past_weekday_expenses]
        if not past_totals:
            return {
                'weekday': weekday_name,
                'comparison_rate': 0
            }
            
        average_past_expense = sum(past_totals) / len(past_totals)
        

        if average_past_expense == 0:
            comparison_rate = 100 if today_expense > 0 else 0
        else:
            comparison_rate = round((today_expense / average_past_expense) * 100)
            
        return {
            'weekday': weekday_name,
            'comparison_rate': comparison_rate
        }

    def _get_other_users_comparison(self, user, today):
        start_of_month = today.replace(day=1)

        my_budget = Expense.objects.filter(
            user=user,
            expense_date__year=today.year,
            expense_date__month=today.month
        ).aggregate(total=Sum('expense_money'))['total'] or 0
        
        my_expense = Expense.objects.filter(
            user=user,
            expense_date__year=today.year,
            expense_date__month=today.month,
            expense_date__lte=today,
            is_excluded=False
        ).aggregate(total=Sum('expense_money'))['total'] or 0
        
        my_usage_rate = (my_expense / my_budget * 100) if my_budget > 0 else 0
        
        other_users_data = Expense.objects.filter(
            user=user,
            expense_date__year=today.year,
            expense_date__month=today.month
        ).values('user').annotate(
            total_expense=Sum(
                'expense_money',
                filter=models.Q(
                    expense_date__year=today.year,
                    expense_date__month=today.month,
                    expense_date__lte=today,
                    is_excluded=False
                )
            )
        ).exclude(total_expense=0)
        
        other_users_rates = []
        for data in other_users_data:
            if data['total_expense']:
                rate = (data['total_expense'] / my_expense) * 100
                other_users_rates.append(rate)
        
        if not other_users_rates:
            return {
                'other_users_rate': 0,
                'my_usage_rate': round(my_usage_rate, 1),
                'average_usage_rate': 0
            }
        
        average_usage_rate = sum(other_users_rates) / len(other_users_rates)
        
        comparison_rate = round((my_usage_rate / average_usage_rate * 100), 1) if average_usage_rate > 0 else 0
        
        return {
            'other_users_rate': comparison_rate,
            'my_usage_rate': round(my_usage_rate, 1),
            'average_usage_rate': round(average_usage_rate, 1)
        }