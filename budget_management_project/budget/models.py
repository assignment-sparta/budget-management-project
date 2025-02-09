from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

CATEGORY_TYPES = [
    ('ETC', '기타'),
    ('FOOD', '식비'),
    ('TRANSPORT', '교통'),
    ('HOUSING', '주거'),
    ('INSURANCE', '보험'),
    ('LOAN', '대출'),
    ('MEDICAL', '건강 및 의료'),
    ('EDUCATION', '자기계발'),
    ('HOBBY', '취미'),
    ('EMERGENCY', '비상금'),
]

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, choices=CATEGORY_TYPES, default='ETC')
    description = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = 'category'


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
        