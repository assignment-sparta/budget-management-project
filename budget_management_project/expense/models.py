from django.db import models
from django.contrib.auth import get_user_model
from budget_management_project.expense.enums import CategoryType

User = get_user_model()


class Category(models.Model):
    type = models.PositiveIntegerField(
        choices=[(name.code, name.description) for name in CategoryType],
        unique=True
    )
    description = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "category"
    
    def __str__(self):
        return CategoryType.from_code(self.type).description


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    expense_money = models.PositiveIntegerField(default=0)
    expense_date = models.DateField(db_index=True)
    memo = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_excluded = models.BooleanField(default=False)

    class Meta:
        db_table = "expense"
        ordering = ['-expense_date', '-created_at']
        indexes = [
            models.Index(fields=['-expense_date', '-created_at'], name='expense_date_created_idx'),
        ]