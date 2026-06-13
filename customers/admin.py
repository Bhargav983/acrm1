from django.contrib import admin

from .models import APIData, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'gender',
        'mobile_number',
        'email',
        'place_of_birth',
        'is_active',
    )
    list_filter = ('gender', 'marital_status', 'is_active')
    search_fields = (
        'customer_name',
        'mobile_number',
        'email',
        'place_of_birth',
        'occupation',
        'education',
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(APIData)
class APIDataAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'data_source',
        'api_provider',
        'api_type',
        'nakshatra',
        'pada',
        'is_active',
    )
    list_filter = ('data_source', 'api_type', 'is_active')
    search_fields = (
        'customer__customer_name',
        'api_provider',
        'api_name',
        'lagna',
        'moon_sign',
        'sun_sign',
        'nakshatra',
    )
    readonly_fields = ('created_at', 'updated_at')
