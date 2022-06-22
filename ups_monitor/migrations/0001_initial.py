# Generated by Django 4.0.5 on 2022-06-09 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UPS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30)),
                ('slug', models.SlugField(max_length=30, unique=True)),
                ('ip', models.CharField(max_length=30)),
                ('port', models.IntegerField(default=2065)),
                ('login', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('descript', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'UPS',
                'verbose_name_plural': 'UPS',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='StateHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_voltage', models.FloatField()),
                ('temperature', models.FloatField()),
                ('charge_battary', models.IntegerField()),
                ('load', models.FloatField()),
                ('working_hours', models.FloatField()),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('ups', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ups_monitor.ups')),
            ],
            options={
                'verbose_name': 'State history UPS',
                'verbose_name_plural': 'State history UPS',
                'ordering': ('ups',),
            },
        ),
        migrations.CreateModel(
            name='ReportHIstory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=30)),
                ('voltage_battary', models.FloatField()),
                ('report_selftest', models.CharField(max_length=2)),
                ('made_date', models.DateField()),
                ('last_date_battary_replacement', models.DateField()),
                ('serial_number', models.CharField(max_length=30)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('ups', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ups_monitor.ups')),
            ],
        ),
    ]
