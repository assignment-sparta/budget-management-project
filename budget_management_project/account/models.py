from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=256, unique=True, help_text='이메일')
    username = models.CharField(max_length=32, unique=True, help_text='유저 네임')
    password = models.CharField(max_length=128, help_text='패스워드')
    created_at = models.DateTimeField(auto_now_add=True, help_text='생성 일시')
    is_active = models.BooleanField(default=True, help_text='활성 상태')

    class Meta:
        db_table = 'user'
