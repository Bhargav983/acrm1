from django.contrib import admin

from .models import ConsultationNote


@admin.register(ConsultationNote)
class ConsultationNoteAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'consultation_date',
        'topic',
        'follow_up_required',
        'follow_up_date',
        'created_by',
        'is_active',
    )
    list_filter = ('topic', 'follow_up_required', 'is_active')
    search_fields = ('customer__customer_name', 'topic', 'notes')
    readonly_fields = ('created_at', 'updated_at')
