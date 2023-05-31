from accounts import models
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'username', 'email', 'is_active', 'is_student', 'is_instructor', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_instructor', 'is_staff']
        
admin.site.register(models.User, UserAdmin)
