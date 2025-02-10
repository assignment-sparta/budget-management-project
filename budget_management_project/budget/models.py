from django.db import models
from django.contrib.auth import get_user_model
from budget_management_project.expense.models import Category

User = get_user_model()


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    budget_amount = models.PositiveIntegerField(default=0)
    budget_date = models.DateField()
    recommended_amount = models.PositiveIntegerField(default=0)
    risk_rate = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'budget'