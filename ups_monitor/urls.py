from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:id>/<str:slug>/', views.detail, name='detail'),
 
]
