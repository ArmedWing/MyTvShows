from django.urls import path
from MyTvShows.seriesapi.views import saved_shows, show_details, increase_counter, add_to_favorites, search_tv_show

urlpatterns = [
    path('series_detail/', saved_shows, name='series_detail'),
    path('add_to_favorites/<str:tvmaze_id>/', add_to_favorites, name='add_to_favorites'),
    path('series_search/', search_tv_show, name='search_tv_show'),
    path('show/increase_counter/<int:pk>/', increase_counter, name='increase_counter'),
    path('show/more_details/<int:pk>/', show_details, name='show_details'),

]