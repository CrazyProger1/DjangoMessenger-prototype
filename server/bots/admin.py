from django.contrib import admin
from .models import *


class BotAdmin(admin.ModelAdmin):
    list_display = ('creator', 'name')


admin.site.register(Bot, BotAdmin)
