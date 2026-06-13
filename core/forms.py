from django import forms

from .models import AppConfig, SettingOption


class SettingOptionForm(forms.ModelForm):
    class Meta:
        model = SettingOption
        fields = [
            'setting_type',
            'name',
            'description',
            'sort_order',
            'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class


class AppConfigForm(forms.ModelForm):
    class Meta:
        model = AppConfig
        fields = [
            'config_type',
            'config_name',
            'provider_name',
            'api_url',
            'api_key',
            'api_secret',
            'sender_email',
            'smtp_host',
            'smtp_port',
            'username',
            'password',
            'is_active',
            'notes',
        ]
        widgets = {
            'api_key': forms.PasswordInput(render_value=True),
            'api_secret': forms.PasswordInput(render_value=True),
            'password': forms.PasswordInput(render_value=True),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class
