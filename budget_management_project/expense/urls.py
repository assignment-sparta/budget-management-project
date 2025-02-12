from django.urls import path

from budget_management_project.expense.views import (
    ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView, 
    ExpenseListView, ExpenseDetailView, ExpenseExcludeView
)

urlpatterns = [
    path('expenses', ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses/<int:expense_id>', ExpenseUpdateView.as_view(), name='expense-update'),
    path('expenses/<int:expense_id>', ExpenseDeleteView.as_view(), name='expense-delete'),
    path('expenses', ExpenseListView.as_view(), name='expense-list'),
    path('expenses/<int:expense_id>', ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/<int:expense_id>/exclude', ExpenseExcludeView.as_view(), name='expense-exclude'),
]