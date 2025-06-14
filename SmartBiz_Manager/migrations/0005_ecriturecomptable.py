# Generated by Django 5.1.6 on 2025-06-01 00:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartBiz_Manager', '0004_alter_vente_date_lignecommande'),
    ]

    operations = [
        migrations.CreateModel(
            name='EcritureComptable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal', models.CharField(choices=[('VT', 'Ventes'), ('AC', 'Achats'), ('BQ', 'Banque')], default='VT', max_length=2)),
                ('date', models.DateField(auto_now_add=True)),
                ('compte_debit', models.CharField(max_length=10)),
                ('compte_credit', models.CharField(max_length=10)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('libelle', models.CharField(max_length=200)),
                ('facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SmartBiz_Manager.facture')),
                ('vente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SmartBiz_Manager.vente')),
            ],
        ),
    ]
