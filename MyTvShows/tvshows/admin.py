from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from MyTvShows.tvshows.models import Profile, Show, Review, Genre, Episode, Season, SeasonEpisodes, Thread, Reply

# admin.site.register(Profile)

admin.site.site_title = "My Custom Admin"
admin.site.site_header = "Welcome to My Custom Admin"
admin.site.index_title = "Manage Shows and More"


class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'day_of_airing',)
    list_filter = ('day_of_airing', 'profile__username')
    search_fields = ('name', 'profile__username')
    list_editable = ('day_of_airing',)


admin.site.register(Show, ShowAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'full_name', 'profile_picture')
    search_fields = ('user__username', 'username', 'first_name', 'last_name')
    list_filter = ('user__is_active',)

    def username(self, obj):
        return obj.user.username

    def full_name(self, obj):
        return obj.full_name()

    username.short_description = 'Username'
    full_name.short_description = 'Full Name'

admin.site.register(Profile, ProfileAdmin)


