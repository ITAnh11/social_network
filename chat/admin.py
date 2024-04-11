from django.contrib import admin
from .models import Message, Conversation

class MessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['sender', 'receiver', 'content', 'is_read', 'created_at']


admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation)
