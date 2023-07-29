from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MyTvShows.tvshows.urls')),
    # path('auth/', include('MyTvShows.tvshows.urls')),
]
