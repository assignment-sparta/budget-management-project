from django.urls import path
from budget import views

app_name = "budget"

urlpatterns = [
    path('categories', views.CategoryView.as_view(), name='category'),
    path('budgets', views.BudgetView.as_view(), name='budget-setting'),
]
