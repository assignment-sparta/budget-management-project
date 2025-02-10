from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "category"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    expense_money = models.PositiveIntegerField(default=0)
    expense_date = models.DateField(auto_now_add=True) 
    memo = models.TextField(null=True, blank=True) 
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True) 

    class Meta:
        db_table = "expense"