# Generated by Django 4.0.5 on 2022-07-08 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gprs_monitor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gprs',
            name='sim',
        ),
    ]
