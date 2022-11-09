from re import I
from django.contrib import admin
from posts.models import Post, Tags, Category


admin.site.register(Post)
admin.site.register(Tags)
admin.site.register(Category)

