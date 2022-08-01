from django.urls import path
from . import views



urlpatterns = [
    path('', views.gprs_list ,name='gprs'),
    path('<str:city_slug>/', views.gprs_list, name='gprs_list_by_city'),
    path('detail/<str:id>/', views.client_datail, name='gprs_client_detail'),

]