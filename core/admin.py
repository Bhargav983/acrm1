from django.contrib import admin

from .models import AppConfig, SettingOption


@admin.register(SettingOption)
class SettingOptionAdmin(admin.ModelAdmin):
    list_display = (
        'setting_type',
        'name',
        'description',
        'sort_order',
        'is_active',
    )
    list_filter = ('setting_type', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AppConfig)
class AppConfigAdmin(admin.ModelAdmin):
    list_display = (
        'config_type',
        'config_name',
        'provider_name',
        'sender_email',
        'smtp_host',
        'is_active',
    )
    list_filter = ('config_type', 'is_active')
    search_fields = ('config_name', 'provider_name', 'api_url', 'sender_email', 'smtp_host')
    readonly_fields = ('created_at', 'updated_at')
