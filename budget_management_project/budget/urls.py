from django.urls import path
from budget_management_project.budget import views

app_name = "budget"

urlpatterns = [
    path('budgets', views.BudgetView.as_view(), name='budget-setting'),
]
