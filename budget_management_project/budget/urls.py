from django.urls import path
from budget_management_project.budget import views

app_name = "budget"

urlpatterns = [
    path('budgets', views.BudgetView.as_view(), name='budget-setting'),
    path('budgets/<int:budget_id>', views.BudgetDetailView.as_view(), name='budget-detail'),
    path('budget/recommends', views.BudgetRecommendView.as_view(), name='budget-recommend'),
]
