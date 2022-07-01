from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('api/state_ups/', views.ups_state_list),
    path('api/detail_ups/<str:ip>/', views.ups_detail),
    path('api/update_datail/<str:ip/', views.update_detail),
    path('<str:id>/<str:slug>/', views.detail, name='detail'),
    path('orders_page/', views.orders_app),
    path('detail_ups/', views.detail_ups)
     
]
