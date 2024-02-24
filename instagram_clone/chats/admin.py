from django.contrib import admin
from .models import Message, Chat


class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'slug', 'chat_to_user', 'date_created', 'updated')
    list_filter = ("author__username",)
    search_fields = ['post__slug', 'auhtor__username']
    prepopulated_fields = {}


class MessageAdmin(admin.ModelAdmin):
    list_display = (    
                    'id', 
                    'author', 
                    'chat',
                    'message',
                    'sent_for',
                    'status',
                    'date_created',
                    'updated'
                )
    list_filter = ("author__username", "sent_for__username")
    search_fields = [   
                     'sent_for__username',
                     'auhtor__username', 
                     'status', 
                     'date_created'
                    ]
    prepopulated_fields = {}

     
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)

