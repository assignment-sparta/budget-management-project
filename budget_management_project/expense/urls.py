from django.urls import path
from budget_management_project.expense import views

urlpatterns = [
    path('categories', views.CategoryView.as_view(), name='category'),
    path('expenses', views.ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses/<int:expense_id>', views.ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/<int:expense_id>/exclude', views.ExpenseExcludeView.as_view(), name='expense-exclude'),
]