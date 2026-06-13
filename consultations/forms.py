from django import forms

from core.settings_utils import get_setting_choices
from customers.models import Customer

from .models import ConsultationNote


class ConsultationNoteForm(forms.ModelForm):
    class Meta:
        model = ConsultationNote
        fields = [
            'customer',
            'consultation_date',
            'topic',
            'notes',
            'follow_up_required',
            'follow_up_date',
            'is_active',
        ]
        widgets = {
            'consultation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(is_active=True)
        if self.instance and self.instance.pk and self.instance.customer_id:
            self.fields['customer'].queryset = (
                Customer.objects.filter(pk=self.instance.customer_id)
                | self.fields['customer'].queryset
            ).distinct()
        self.fields['topic'].choices = get_setting_choices(
            'Consultation Topic',
            fallback_choices=ConsultationNote.TOPIC_CHOICES,
            include_blank=False,
            current_value=self.instance.topic if self.instance.pk else None,
        )
        self.fields['topic'].widget.choices = self.fields['topic'].choices

        for field in self.fields.values():
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class
