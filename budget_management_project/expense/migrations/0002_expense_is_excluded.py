# Generated by Django 5.1.5 on 2025-02-13 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='is_excluded',
            field=models.BooleanField(default=False),
        ),
    ]
