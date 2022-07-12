from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.gprs ,name='gprs'),

]