from django.urls import path

from . import views

urlpatterns = [
    path('wine/', views.dummy, name='api-wine-detail-base'),
    path('wine/<str:wine_id>/', views.dummy, name='api-wine-detail'),
    path('wine/ml/', views.dummy, name='api-wine-ml-base'),

    path('wine/ml/<str:wine_id>/similar/', views.wine_recommender_similarity, name='api-wine-ml-similar'),
    path('wine/ml/predict_do/', views.predict_do, name='api-wine-ml-predictdo'),
]
