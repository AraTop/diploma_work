from django.contrib import admin
from main.models import Payment, Сhannel , Post, Сomments, Subscriptions

@admin.register(Сhannel)
class СhannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'profile_icon')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_post', 'description', 'subscription_level' , 'likes' , 'time_the_comment', 'channel')


@admin.register(Сomments)
class СommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'time_the_comment', 'post')


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'strength_of_subscription', 'amount_per_month', 'channel')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user_nickname', 'payment_date', 'subscriptions', 'amount', 'payment_method')
