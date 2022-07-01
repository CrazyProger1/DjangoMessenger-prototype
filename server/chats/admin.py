from django.contrib import admin

from .models import *


class ChatAdmin(admin.ModelAdmin):
    list_display = ('creator', 'group')


class ChatMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'bot', 'chat')


admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatMember, ChatMemberAdmin)
