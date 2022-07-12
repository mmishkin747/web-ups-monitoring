# Generated by Django 4.0.5 on 2022-07-08 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gprs_monitor', '0002_remove_gprs_sim'),
    ]

    operations = [
        migrations.AddField(
            model_name='gprs',
            name='operator_sim',
            field=models.CharField(blank=True, choices=[('GOLD', 'Gold'), ('SILVER', 'Silver'), ('BRONZE', 'Bronze')], max_length=10),
        ),
    ]
