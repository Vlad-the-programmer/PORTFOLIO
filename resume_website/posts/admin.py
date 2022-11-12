from re import I
from django.contrib import admin
from posts.models import Post, Tags, Category

class CategoryAdmin(admin.ModelAdmin):
     prepopulated_fields = {"slug": ("name",)}
     
class PostAdmin(admin.ModelAdmin):
     prepopulated_fields = {"slug": ("title",)}
     
admin.site.register(Post, PostAdmin)
admin.site.register(Tags)
admin.site.register(Category, CategoryAdmin)

