from django.contrib import admin
from .models import Post, Idea, Theme

admin.site.register(Theme)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    filter_horizontal = ('themes',)


@admin.register(Idea)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post', 'title')
