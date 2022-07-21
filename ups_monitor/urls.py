from django.urls import path, include

from . import views



urlpatterns = [
    path('', views.index ,name='index'),
    path('ups/', views.ups_list),
    path('<str:ip>/', views.detail, name='detail'),
    path('api/state_ups/', views.ups_state_list),
    path('api/detail_ups/<str:ip>/', views.ups_detail),
    path('api/update_detail/<str:ip>/', views.update_detail),
    
    path('orders_page/', views.orders_app),
    path('detail_ups/', views.detail_ups),
]
