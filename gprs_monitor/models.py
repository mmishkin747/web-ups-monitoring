from pyexpat import model
from tabnanny import verbose
from django.db import models

# Create your models here.

class GprsCity(models.Model):
    city = models.CharField(max_length=100)

    class Meta:
        ordering = ('city',)
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city

class Gprs(models.Model):
    Operators= models.TextChoices('operators', 'A1 MTS life')
    city = models.ForeignKey(GprsCity, on_delete=models.CASCADE)
    client = models.CharField(max_length=100)
    login_bft = models.CharField(max_length=100)
    password_bft = models.CharField(max_length=100)
    ppp = models.CharField(max_length=100)
    login_ftp = models.CharField(max_length=100)
    password_ftp = models.CharField(max_length=100)
    type_modem = models.CharField(max_length=100)
    imei_modem = models.CharField(max_length=100)
    operator_sim = models.CharField(blank=True, choices=Operators.choices, max_length=10)
    number_sim = models.CharField(max_length=100)
    email_client = models.EmailField()
    date_con = models.DateField()
    description = models.CharField(max_length=300)