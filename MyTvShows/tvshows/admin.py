from django.contrib import admin


from MyTvShows.tvshows.models import Show, Review, Thread, Reply, Episode

admin.site.site_title = "My Custom Admin"
admin.site.site_header = "Welcome to My Custom Admin"
admin.site.index_title = "Manage Shows and More"


class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'day_of_airing',)
    list_filter = ('day_of_airing', 'profile__username')
    search_fields = ('name', 'profile__username')
    list_editable = ('day_of_airing',)


admin.site.register(Show, ShowAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'series', 'rating')
    list_filter = ('rating', 'series')
    search_fields = ('author__username', 'series__name')


admin.site.register(Review, ReviewAdmin)


class ReplyInline(admin.StackedInline):
    model = Reply

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    date_hierarchy = 'created_at'
    inlines = [ReplyInline]

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply)


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('series', 'episode_number')
    list_filter = ('series__name',)
    search_fields = ('title', 'description', 'series__name')

admin.site.register(Episode, EpisodeAdmin)
