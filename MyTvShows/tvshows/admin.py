from django.contrib import admin

from django.forms import TextInput, Textarea
from django.db import models
from MyTvShows.tvshows.models import Show, Review, Thread, Reply, Episode, Genre

admin.site.site_title = "My Custom Admin"
admin.site.site_header = "Welcome to My Custom Admin"
admin.site.index_title = "Manage Shows and More"


class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'day_of_airing', 'user', 'description')
    list_filter = ('day_of_airing', 'profile__username')
    search_fields = ('name', 'profile__username')
    list_editable = ('day_of_airing', 'description')

    # this allows me to change the sizeof the fields
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

admin.site.register(Show, ShowAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'series', 'rating')
    list_filter = ('rating', 'series')
    search_fields = ('author__username', 'series__name')


admin.site.register(Review, ReviewAdmin)


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author', 'created_at')
    search_fields = ('title', 'author__username')

    date_hierarchy = 'created_at'


admin.site.register(Thread, ThreadAdmin)

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('series', 'episodes_watched')
    list_filter = ('series__name',)
    search_fields = ('title', 'description')

admin.site.register(Episode, EpisodeAdmin)


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'thread', 'content' )
    list_filter = ('author', 'thread')
    search_fields = ('author', 'thread')


admin.site.register(Reply, ReplyAdmin)