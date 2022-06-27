from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wine-list/', views.wine_list, name='wine-list'),
    path('wine/', views.wine_detail, name='wine-detail-base'),
    path('wine/<str:wine_id>/', views.wine_detail, name='wine-detail'),
    path('find-wine/', views.find_wine, name='find-wine'),
]
