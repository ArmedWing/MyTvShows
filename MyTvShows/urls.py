from django.contrib import admin
from django.urls import path, include


from MyTvShows.tvshows.views import custom_404

handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MyTvShows.tvshows.urls')),
    path('', include('MyTvShows.seriesapi.urls')),
    # path('auth/', include('MyTvShows.tvshows.urls')),

]



