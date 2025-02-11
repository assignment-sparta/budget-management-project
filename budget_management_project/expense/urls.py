from django.urls import path

from expense.views import ExpenseCreateView, ExpenseUpdateView

app_name = "expense"

urlpatterns = [
    path('api/v1/expenses', ExpenseCreateView.as_view(), name='expense-create'),
    path('api/v1/expenses/<int:expense_id>', ExpenseUpdateView.as_view(), name='expense-update'),
]