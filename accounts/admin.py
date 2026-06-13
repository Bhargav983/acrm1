from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Role, User


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        'role_name',
        'can_view',
        'can_add',
        'can_edit',
        'can_delete',
        'is_active',
    )
    list_filter = ('is_active', 'can_view', 'can_add', 'can_edit', 'can_delete')
    search_fields = ('role_name', 'description')


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('CRM Profile', {'fields': ('full_name', 'mobile_number', 'role')}),
        ('Audit', {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('CRM Profile', {'fields': ('full_name', 'mobile_number', 'role')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    list_display = (
        'username',
        'full_name',
        'email',
        'mobile_number',
        'role',
        'is_active',
        'is_staff',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'role')
    search_fields = ('username', 'full_name', 'email', 'mobile_number')
