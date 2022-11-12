from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile

class CustomUserAdmin(UserAdmin):
    model = Profile
    list_display = ['email', 'username', 'featured_img', 'first_name', 'last_name', 'country', 'is_active', 'is_staff']

admin.site.register(Profile, CustomUserAdmin)
