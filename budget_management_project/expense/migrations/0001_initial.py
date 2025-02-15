# Generated by Django 5.1.5 on 2025-02-13 19:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveIntegerField(choices=[(1, '기타'), (2, '학비'), (3, '교재비'), (4, '인강비'), (5, '통신요금'), (6, '식비'), (7, '대중교통비'), (8, '여가생활비'), (9, '자기개발비'), (10, '동아리 비용'), (11, '개인 물품비'), (12, '기숙사비'), (13, '건강 비용')], unique=True)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_money', models.PositiveIntegerField(default=0)),
                ('expense_date', models.DateField(db_index=True)),
                ('memo', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_excluded', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'expense',
                'ordering': ['-expense_date', '-created_at'],
                'indexes': [models.Index(fields=['-expense_date', '-created_at'], name='expense_date_created_idx')],
            },
        ),
    ]
