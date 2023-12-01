from django.contrib import admin
from main.models import Сhannel


@admin.register(Сhannel)
class СhannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'profile_icon')
