from django.contrib import admin
from subscription.models import Subscriptions


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'strength_of_subscription', 'amount_per_month', 'channel')
