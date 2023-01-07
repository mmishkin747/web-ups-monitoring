from django.urls import path

from . import views



urlpatterns = [
    path('', views.index ,name='index'),
    path('ups/', views.ups_list),
    path('<str:ip>/', views.detail, name='detail'),
    path('api/state_ups/', views.UpsStateList.as_view()),
    path('api/check_now/<str:ip>/', views.CheckStateNow.as_view()),
    path('api/update_detail/<str:ip>/', views.UpdateDetail.as_view()), 
    path('api/notiPRTG/', views.NotiPRTG.as_view()),
]


#-----------------------------------------------------------------------

    #path('api/detail_ups/<str:ip>/', views.ups_detail), #future