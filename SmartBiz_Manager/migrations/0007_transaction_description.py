# Generated by Django 5.1.6 on 2025-06-07 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartBiz_Manager', '0006_department_budget_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.TextField(default='aucune description'),
        ),
    ]
