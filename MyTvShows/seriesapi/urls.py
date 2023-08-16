from django.urls import path

from MyTvShows.seriesapi import views
from MyTvShows.seriesapi.views import saved_shows



urlpatterns = [
    path('series_detail/', saved_shows, name='series_detail'),
    path('add_to_favorites/<str:imdb_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('series_search/', views.search_tv_show, name='search_tv_show'),

]