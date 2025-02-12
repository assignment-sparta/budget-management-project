from django.urls import path
from budget_management_project.expense import views  # views 모듈 전체를 import

app_name = "expense"

urlpatterns = [
    path('categories', views.CategoryView.as_view(), name='category'),
    path('expenses', views.ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses/<int:expense_id>', views.ExpenseUpdateView.as_view(), name='expense-update'),
]