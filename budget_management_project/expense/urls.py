from django.urls import path
from budget_management_project.expense import views  # views 모듈 전체를 import


urlpatterns = [
    path('categories', views.CategoryView.as_view(), name='category'),
    path('expenses', views.ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses/<int:expense_id>', views.ExpenseUpdateView.as_view(), name='expense-update'),
    path('expenses/<int:expense_id>', views.ExpenseDeleteView.as_view(), name='expense-delete'),
    path('expenses', views.ExpenseListView.as_view(), name='expense-list'),
    path('expenses/<int:expense_id>', views.ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/<int:expense_id>/exclude', views.ExpenseExcludeView.as_view(), name='expense-exclude'),
]