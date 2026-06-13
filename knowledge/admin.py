from django.contrib import admin

from .models import (
    AstrologyKnowledge,
    Category,
    CustomerKnowledgeTracking,
    CustomerResearchAnswer,
    HypothesisQuestion,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('category_name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AstrologyKnowledge)
class AstrologyKnowledgeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'system',
        'category',
        'section',
        'knowledge_type',
        'life_areas',
        'status',
        'nature',
        'confidence_level',
        'is_active',
    )
    list_filter = (
        'system',
        'category',
        'section',
        'knowledge_type',
        'status',
        'nature',
        'confidence_level',
        'is_active',
    )
    search_fields = (
        'title',
        'description',
        'short_meaning',
        'life_areas',
        'applies_to_name',
        'applies_to_subtype',
        'related_factor',
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(HypothesisQuestion)
class HypothesisQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'hypothesis',
        'question_type',
        'sort_order',
        'is_active',
    )
    list_filter = ('question_type', 'is_active')
    search_fields = ('hypothesis__title', 'question_text')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CustomerResearchAnswer)
class CustomerResearchAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'hypothesis',
        'question',
        'answer_value',
        'answered_by',
        'answered_date',
    )
    list_filter = ('answered_date', 'question__question_type')
    search_fields = (
        'customer__customer_name',
        'hypothesis__title',
        'question__question_text',
        'answer_text',
        'answer_value',
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CustomerKnowledgeTracking)
class CustomerKnowledgeTrackingAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'knowledge',
        'tracking_type',
        'status',
        'effectiveness_rating',
        'outcome',
        'verified_by',
        'is_active',
    )
    list_filter = ('tracking_type', 'status', 'outcome', 'is_active')
    search_fields = (
        'customer__customer_name',
        'knowledge__title',
        'customer_feedback',
        'researcher_notes',
    )
    readonly_fields = ('created_at', 'updated_at')
