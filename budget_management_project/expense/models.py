from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

#대학생
CATEGORY_TYPES = [
    ('ETC', '기타'),
    ('tuition_fee', '학비'),
    ('book_fee', '교재비'),
    ('courses_fee', '인강비'),
    ('communication_fee', '통신요금'),
    ('food_fee', '식비'),
    ('transportation_fee', '대중교통비'),
    ('leisure_fee', '여가생활비'),
    ('self_development_fee', '자기개발비'),
    ('club_fee', '동아리 비용'),
    ('preparation_fee', '개인 물품비'),
    ('dormitory_fee', '기숙사비'),
    ('healthcare_fee', '건강 비용'),
]
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50, choices=CATEGORY_TYPES, default='ETC')
    description = models.CharField(max_length=50, null=True, blank=True)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    expense_money = models.PositiveIntegerField(default=0)
    expense_date = models.DateField(auto_now_add=True) #임시로 DateField 설정
    memo = models.TextField(null=True, blank=True) 
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True) #임시로 DateField 설정

    
    
#-----------------------------------------------------------------------
#직장인
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