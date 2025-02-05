from django.db import models
from django.contrib.auth.models import AbstractUser

#사용자 모델 등록
class User(AbstractUser):
    email = models.EmailField('이메일', max_length=256, unique=True)
    username = models.CharField('유저 내임', max_length=32, unique=True)
    password = models.CharField('패스워드', max_length=32)
    created_at = models.DateTimeField('생성 일시', auto_now_add=True)
    is_active = models.BooleanField('활성 상태', default=True)