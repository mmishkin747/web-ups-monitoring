# Generated by Django 4.0.5 on 2022-07-28 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gprs_monitor', '0004_alter_gprs_operator_sim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gprs',
            name='date_con',
            field=models.CharField(max_length=300),
        ),
    ]