from django.urls import path

from . import views

urlpatterns = [
    path('wine/', views.dummy, name='api-wine-detail-base'),
    path('wine/<str:wine_id>/', views.wine_detail, name='api-wine-detail'),
    path('wines/', views.wine_list, name='api-wine-list'),
    path('wines/search/', views.wine_search, name='api-wine-search'),
    path('zones/', views.do_list, name='api-do-list'),

    path('wine/ml/', views.dummy, name='api-wine-ml-base'),
    path('wine/ml/<str:wine_id>/similar/', views.wine_recommender_similarity, name='api-wine-ml-similar'),
    path('wine/ml/predict_do/', views.predict_do, name='api-wine-ml-predictdo'),
    path('wine/ml/recomend_wines/', views.wine_recommender_style_do, name='api-wine-ml-recommend-wines'),
]
