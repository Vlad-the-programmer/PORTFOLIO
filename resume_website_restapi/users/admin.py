from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


Profile = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['id',
                    'email',
                    'username',
                    'featured_img',
                    'first_name',
                    'last_name',
                    'country',
                    'gender',
                    'is_superuser',
                    'is_active',
                    'is_staff',
                    'date_joined',
                    'last_login',
                    ]
    list_filter = ()
    search_fields = ['email', 'username']
    
    
admin.site.register(Profile, CustomUserAdmin)