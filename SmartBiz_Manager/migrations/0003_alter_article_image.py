# Generated by Django 5.1.3 on 2025-05-29 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartBiz_Manager', '0002_categorie_vente_facture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='articles/'),
        ),
    ]
