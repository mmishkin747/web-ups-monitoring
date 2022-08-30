from ast import arg
from datetime import datetime, date
from json import load
from django.urls import reverse
from django.utils import timezone
from django.db import models


# Create your models here.

class UPS(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    ip = models.CharField(max_length=30)
    port = models.IntegerField(default=2065)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    descript = models.CharField(max_length=30)


    class Meta:
        ordering = ('name',)
        verbose_name = 'UPS'
        verbose_name_plural = 'UPS'

    def __str__(self):
        return self.name

    


class StateHistory(models.Model):
    ups = models.ForeignKey(UPS, on_delete=models.CASCADE)
    main_voltage = models.FloatField()
    temperature = models.FloatField()
    charge_battary = models.IntegerField()
    load = models.FloatField()
    working_hours = models.FloatField()
    low_main_voltage = models.BooleanField(default=False)
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('ups',)
        verbose_name = 'State history UPS'
        verbose_name_plural = 'State history UPS'

    def get_absolute_url(self):
        return reverse('ups_monitor:detail', args=[self.ups.ip])


class ReportHIstory(models.Model):
    ups = models.ForeignKey(UPS, on_delete=models.CASCADE)
    model = models.CharField(max_length=30, default='None') 
    voltage_battary = models.FloatField(default=0.0)
    report_selftest = models.CharField(max_length=2, default='NA',)
    made_date = models.DateField(default=timezone.now,)
    last_date_battary_replacement = models.DateField(default=timezone.now,)
    serial_number = models.CharField(max_length=30, default='sn0000000')
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('ups',)
        verbose_name = 'Report history UPS'
        verbose_name_plural = 'Report history UPS'


class ErrorUPS(models.Model):
    ups = models.ForeignKey(UPS, on_delete=models.CASCADE)
    error_con = models.BooleanField(default=False)
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_add',)
        verbose_name = 'Error UPS'
        verbose_name_plural = 'Errors UPS'
