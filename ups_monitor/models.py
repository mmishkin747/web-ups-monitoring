from ast import arg
from datetime import datetime
from django.urls import reverse
from django.db import models

# Create your models here.

class UPS(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    slug = models.SlugField(max_length=30, db_index=True, unique=True)
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
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('ups',)
        verbose_name = 'State history UPS'
        verbose_name_plural = 'State history UPS'

    def get_absolute_url(self):
        return reverse('ups_monitor:detail', args=[self.ups.id, self.ups.slug])


class ReportHIstory(models.Model):
    ups = models.ForeignKey(UPS, on_delete=models.CASCADE)
    model = models.CharField(max_length=30) 
    voltage_battary = models.FloatField()
    report_selftest = models.CharField(max_length=2)
    made_date = models.DateField()
    last_date_battary_replacement = models.DateField()
    serial_number = models.CharField(max_length=30)
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('ups',)
        verbose_name = 'Report history UPS'
        verbose_name_plural = 'Report history UPS'


