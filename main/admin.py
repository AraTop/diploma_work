from django.contrib import admin
from main.models import Сhannel , Post, Сomments, Subscriptions

@admin.register(Сhannel)
class СhannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'profile_icon', 'subscriptions' , 'post')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_post', 'description', 'subscription_level' , 'comments', 'likes' , 'time_the_comment')


@admin.register(Сomments)
class СommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'likes', 'description', 'time_the_comment')


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'profile_icon', 'strength_of_subscription', 'amount_per_month')
