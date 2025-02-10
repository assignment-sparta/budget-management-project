from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "category"
    
    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')
    expense_money = models.PositiveIntegerField(default=0)
    expense_date = models.DateField()
    memo = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "expense"
        ordering = ['-expense_date', '-created_at']

    def __str__(self):
        return f"{self.user.username}의 지출: {self.expense_money}원 ({self.expense_date})"