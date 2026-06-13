from django import forms
from django.forms import modelformset_factory
from django.utils import timezone

from django.contrib.auth import get_user_model

from core.settings_utils import get_setting_choices
from customers.models import Customer

from .models import (
    AstrologyKnowledge,
    Category,
    CustomerKnowledgeTracking,
    CustomerResearchAnswer,
    HypothesisQuestion,
)


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class


class CategoryForm(BootstrapModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class AstrologyKnowledgeForm(BootstrapModelForm):
    class Meta:
        model = AstrologyKnowledge
        fields = [
            'system',
            'category',
            'section',
            'knowledge_type',
            'applies_to_type',
            'applies_to_name',
            'applies_to_subtype',
            'related_factor',
            'title',
            'short_meaning',
            'description',
            'verification_question',
            'expected_result',
            'life_areas',
            'nature',
            'confidence_level',
            'status',
            'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'verification_question': forms.Textarea(attrs={'rows': 3}),
            'expected_result': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['knowledge_type'].label = 'Rule Type'
        categories = Category.objects.filter(is_active=True)
        if self.instance and self.instance.pk and self.instance.category_id:
            categories = Category.objects.filter(
                pk__in=[self.instance.category_id]
            ) | categories
        self.fields['category'].queryset = categories.distinct()
        if not self.instance.pk and categories.exists():
            self.fields['category'].initial = categories.first()
        self.fields['category'].widget = forms.HiddenInput()
        self.fields['section'].choices = get_setting_choices(
            'Section',
            fallback_choices=AstrologyKnowledge.SECTION_CHOICES,
            include_blank=False,
            current_value=self.instance.section if self.instance.pk else None,
        )
        self.fields['section'].widget.choices = self.fields['section'].choices
        self.fields['knowledge_type'].choices = get_setting_choices(
            'Knowledge Type',
            fallback_choices=AstrologyKnowledge.KNOWLEDGE_TYPE_CHOICES,
            include_blank=False,
            current_value=self.instance.knowledge_type if self.instance.pk else None,
        )
        self.fields['knowledge_type'].widget.choices = self.fields['knowledge_type'].choices
        self.fields['applies_to_type'].choices = get_setting_choices(
            'Applies To Type',
            fallback_choices=AstrologyKnowledge.APPLIES_TO_TYPE_CHOICES,
            include_blank=False,
            current_value=self.instance.applies_to_type if self.instance.pk else None,
        )
        self.fields['applies_to_type'].widget.choices = self.fields['applies_to_type'].choices
        self.fields['related_factor'].widget = forms.Select()
        self.fields['related_factor'].choices = get_setting_choices(
            'Related Factor',
            current_value=self.instance.related_factor if self.instance.pk else None,
        )
        self.fields['related_factor'].widget.choices = self.fields['related_factor'].choices
        self.fields['applies_to_type'].widget = forms.HiddenInput()
        self.fields['applies_to_name'].widget = forms.HiddenInput()
        self.fields['applies_to_subtype'].widget = forms.HiddenInput()
        self.fields['related_factor'].widget = forms.HiddenInput()
        self.fields['life_areas'].widget = forms.HiddenInput()
        self.fields['confidence_level'].widget = forms.HiddenInput()
        self.fields['title'].widget.attrs['placeholder'] = 'e.g. Ketu in 12th House'
        self.fields['short_meaning'].widget.attrs['placeholder'] = 'One-line summary used in the list view.'
        self.fields['description'].widget.attrs['placeholder'] = 'Full explanation, references, classical sources...'
        self.fields['expected_result'].widget.attrs['placeholder'] = "What manifests in the native's life."
        self.fields['verification_question'].widget.attrs['placeholder'] = "Private notes for researchers - won't be shown to clients."


class HypothesisQuestionForm(BootstrapModelForm):
    class Meta:
        model = HypothesisQuestion
        fields = [
            'question_text',
            'question_type',
            'sort_order',
            'is_active',
        ]
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 2}),
        }


HypothesisQuestionFormSet = modelformset_factory(
    HypothesisQuestion,
    form=HypothesisQuestionForm,
    extra=5,
    can_delete=False,
)


class CustomerKnowledgeTrackingForm(BootstrapModelForm):
    class Meta:
        model = CustomerKnowledgeTracking
        fields = [
            'customer',
            'knowledge',
            'tracking_type',
            'status',
            'customer_feedback',
            'researcher_notes',
            'start_date',
            'end_date',
            'follow_up_date',
            'effectiveness_rating',
            'outcome',
            'verified_by',
            'verified_date',
            'is_active',
        ]
        widgets = {
            'customer_feedback': forms.Textarea(attrs={'rows': 4}),
            'researcher_notes': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'verified_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(is_active=True)
        self.fields['knowledge'].queryset = AstrologyKnowledge.objects.filter(is_active=True)
        self.fields['verified_by'].queryset = get_user_model().objects.filter(is_active=True)
        tracking_type_choices = get_setting_choices(
            'Tracking Type',
            fallback_choices=CustomerKnowledgeTracking.TRACKING_TYPE_CHOICES,
            include_blank=False,
            current_value=self.instance.tracking_type if self.instance.pk else None,
        )
        status_choices = (
            get_setting_choices('Verification Status', include_blank=False)
            + get_setting_choices('Remedy Status', include_blank=False)
            + get_setting_choices('Research Status', include_blank=False)
        )
        if not status_choices:
            status_choices = list(CustomerKnowledgeTracking.STATUS_CHOICES)
        if self.instance and self.instance.pk and self.instance.status not in [value for value, _label in status_choices]:
            status_choices.append((self.instance.status, self.instance.status))
        outcome_choices = get_setting_choices(
            'Outcome',
            fallback_choices=CustomerKnowledgeTracking.OUTCOME_CHOICES,
            include_blank=True,
            current_value=self.instance.outcome if self.instance.pk else None,
        )
        self.fields['tracking_type'].choices = tracking_type_choices
        self.fields['status'].choices = status_choices
        self.fields['outcome'].choices = outcome_choices
        self.fields['tracking_type'].widget.choices = self.fields['tracking_type'].choices
        self.fields['status'].widget.choices = self.fields['status'].choices
        self.fields['outcome'].widget.choices = self.fields['outcome'].choices

        if self.instance and self.instance.pk:
            if self.instance.customer_id:
                self.fields['customer'].queryset = (
                    Customer.objects.filter(pk=self.instance.customer_id)
                    | self.fields['customer'].queryset
                ).distinct()
            if self.instance.knowledge_id:
                self.fields['knowledge'].queryset = (
                    AstrologyKnowledge.objects.filter(pk=self.instance.knowledge_id)
                    | self.fields['knowledge'].queryset
                ).distinct()
            if self.instance.verified_by_id:
                self.fields['verified_by'].queryset = (
                    get_user_model().objects.filter(pk=self.instance.verified_by_id)
                    | self.fields['verified_by'].queryset
                ).distinct()


class ResearchInterviewSelectForm(forms.Form):
    hypothesis = forms.ModelChoiceField(
        queryset=AstrologyKnowledge.objects.none(),
        label='Research Hypothesis',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hypothesis'].queryset = (
            AstrologyKnowledge.objects.filter(is_active=True)
            .order_by('title')
        )
        self.fields['hypothesis'].widget.attrs['class'] = 'form-select'


class ResearchInterviewForm(forms.Form):
    FINAL_STATUS_CHOICES = [
        ('applies', 'Applies'),
        ('partially_applies', 'Partially Applies'),
        ('does_not_apply', 'Does Not Apply'),
        ('not_asked', 'Not Asked'),
    ]

    final_status = forms.ChoiceField(
        choices=FINAL_STATUS_CHOICES,
        initial='not_asked',
        label='Final Result',
    )
    researcher_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
    )
    verified_date = forms.DateField(
        required=False,
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in self.questions:
            field_name = self.answer_field_name(question)
            notes_name = self.notes_field_name(question)
            if question.question_type == 'yes_no':
                field = forms.ChoiceField(
                    choices=[('', '---------'), ('yes', 'Yes'), ('no', 'No')],
                    required=False,
                    label=question.question_text,
                )
            elif question.question_type == 'rating':
                field = forms.IntegerField(
                    required=False,
                    min_value=1,
                    max_value=10,
                    label=question.question_text,
                )
            else:
                field = forms.CharField(
                    required=False,
                    label=question.question_text,
                    widget=forms.Textarea(attrs={'rows': 3}),
                )
            self.fields[field_name] = field
            self.fields[notes_name] = forms.CharField(
                required=False,
                label='Notes',
                widget=forms.Textarea(attrs={'rows': 2}),
            )

        for field in self.fields.values():
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class

    @staticmethod
    def answer_field_name(question):
        return f'answer_{question.pk}'

    @staticmethod
    def notes_field_name(question):
        return f'notes_{question.pk}'


class TrackingQuestionAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in self.questions:
            field_name = self.answer_field_name(question)
            notes_name = self.notes_field_name(question)
            if question.question_type == 'yes_no':
                field = forms.ChoiceField(
                    choices=[('', '---------'), ('yes', 'Yes'), ('no', 'No')],
                    required=False,
                    label=question.question_text,
                )
            elif question.question_type == 'rating':
                field = forms.IntegerField(
                    required=False,
                    min_value=1,
                    max_value=10,
                    label=question.question_text,
                )
            else:
                field = forms.CharField(
                    required=False,
                    label=question.question_text,
                    widget=forms.Textarea(attrs={'rows': 3}),
                )
            self.fields[field_name] = field
            self.fields[notes_name] = forms.CharField(
                required=False,
                label='Notes',
                widget=forms.Textarea(attrs={'rows': 2}),
            )

        for field in self.fields.values():
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class

    @staticmethod
    def answer_field_name(question):
        return f'answer_{question.pk}'

    @staticmethod
    def notes_field_name(question):
        return f'notes_{question.pk}'
