from django import forms

from .models import Role, User


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class


class RoleForm(BootstrapModelForm):
    class Meta:
        model = Role
        fields = [
            'role_name',
            'description',
            'can_view',
            'can_add',
            'can_edit',
            'can_delete',
            'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class UserCreateForm(BootstrapModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'full_name',
            'username',
            'email',
            'mobile_number',
            'role',
            'password',
            'is_active',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.filter(is_active=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserUpdateForm(BootstrapModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        help_text='Leave blank to keep the existing password.',
    )

    class Meta:
        model = User
        fields = [
            'full_name',
            'username',
            'email',
            'mobile_number',
            'role',
            'password',
            'is_active',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_password = self.instance.password
        roles = Role.objects.filter(is_active=True)
        if self.instance and self.instance.pk and self.instance.role_id:
            roles = Role.objects.filter(pk=self.instance.role_id) | roles
        self.fields['role'].queryset = roles.distinct()

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        else:
            user.password = self._original_password
        if commit:
            user.save()
        return user
