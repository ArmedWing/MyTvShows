from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from MyTvShows.tvshows.models import Thread, Reply, TVShow, Rating

admin.site.site_title = "My Custom Admin"
admin.site.site_header = "Welcome to My Custom Admin"
admin.site.index_title = "Manage Shows and More"


class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'seasons', 'description', 'episodes_watched')
    list_filter = ('year', 'genre')
    search_fields = ('title', 'genre')
    list_editable = ('episodes_watched', 'description')

    # this allows me to change the size of the fields
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

admin.site.register(TVShow, ShowAdmin)


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author', 'created_at')
    search_fields = ('title', 'author__username')

    date_hierarchy = 'created_at'


admin.site.register(Thread, ThreadAdmin)


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'thread', 'content' )
    list_filter = ('author', 'thread')
    search_fields = ('author', 'thread')


admin.site.register(Reply, ReplyAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('rating_value', 'tv_show_id', 'user_id' )
    list_filter = ('rating_value',)
    search_fields = ('tv_show_id', 'rating_value')


admin.site.register(Rating, RatingAdmin)


