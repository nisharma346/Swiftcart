from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom User Admin for managing users
    """
    list_display = (
        'username', 'email', 'full_name', 'mobile_no', 
        'gender', 'is_active', 'is_staff', 'created_at'
    )
    
    list_filter = (
        'is_active', 'is_staff', 'is_superuser', 
        'gender', 'created_at', 'is_email_verified'
    )
    
    search_fields = (
        'username', 'email', 'full_name', 
        'mobile_no', 'alternate_mobile_no'
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Login Information', {
            'fields': ('username', 'password', 'email')
        }),
        ('Personal Information', {
            'fields': (
                'full_name', 'first_name', 'last_name',
                'gender', 'dob', 'profile_image'
            )
        }),
        ('Contact Information', {
            'fields': (
                'mobile_no', 'alternate_mobile_no', 'address'
            )
        }),
        ('Verification', {
            'fields': ('is_email_verified',)
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'full_name', 'mobile_no'
            ),
        }),
    )
