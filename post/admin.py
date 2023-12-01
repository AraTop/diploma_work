from django.contrib import admin
from post.models import Post, Сomments


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_post', 'description', 'subscription_level', 'likes', 'time_the_comment', 'channel')


@admin.register(Сomments)
class СommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'time_the_comment', 'post')
