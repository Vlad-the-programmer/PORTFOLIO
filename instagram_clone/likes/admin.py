from django.contrib import admin
from .models import Like


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'timestamp')
    list_filter = ("author__username",)
    search_fields = ['post__slug', 'auhtor__username']
    prepopulated_fields = {}

     
admin.site.register(Like, LikeAdmin)

