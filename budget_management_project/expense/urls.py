from django.urls import path
from .views import ExpenseCreateView, ExpenseUpdateView

app_name = "expense"

urlpatterns = [
    path('api/v1/expense/', ExpenseCreateView.as_view(), name='expense-create'),
    path('api/v1/expense/<int:expense_id>/', ExpenseUpdateView.as_view(), name='expense-update'),
]