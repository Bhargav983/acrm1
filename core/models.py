from django.conf import settings
from django.db import models


class SettingOption(models.Model):
    SETTING_TYPE_CHOICES = [
        ('Occupation', 'Occupation'),
        ('Education', 'Education'),
        ('Marital Status', 'Marital Status'),
        ('Gender', 'Gender'),
        ('Timezone', 'Timezone'),
        ('Consultation Topic', 'Consultation Topic'),
        ('Knowledge Type', 'Knowledge Type'),
        ('Section', 'Section'),
        ('Applies To Type', 'Applies To Type'),
        ('Related Factor', 'Related Factor'),
        ('Tracking Type', 'Tracking Type'),
        ('Verification Status', 'Verification Status'),
        ('Remedy Status', 'Remedy Status'),
        ('Research Status', 'Research Status'),
        ('Outcome', 'Outcome'),
        ('Role Type', 'Role Type'),
    ]

    setting_type = models.CharField(max_length=100, choices=SETTING_TYPE_CHOICES)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='settings_created',
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='settings_updated',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['setting_type', 'sort_order', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['setting_type', 'name'],
                name='unique_setting_option_type_name',
            ),
        ]

    def __str__(self):
        return f'{self.setting_type}: {self.description or self.name}'


class AppConfig(models.Model):
    CONFIG_TYPE_CHOICES = [
        ('Astrology API', 'Astrology API'),
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('WhatsApp', 'WhatsApp'),
        ('General', 'General'),
    ]

    config_type = models.CharField(max_length=50, choices=CONFIG_TYPE_CHOICES)
    config_name = models.CharField(max_length=150)
    provider_name = models.CharField(max_length=150, blank=True)
    api_url = models.URLField(blank=True)
    api_key = models.CharField(max_length=255, blank=True)
    api_secret = models.CharField(max_length=255, blank=True)
    sender_email = models.EmailField(blank=True)
    smtp_host = models.CharField(max_length=150, blank=True)
    smtp_port = models.PositiveIntegerField(null=True, blank=True)
    username = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='app_configs_created',
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='app_configs_updated',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['config_type', 'config_name']

    def __str__(self):
        return f'{self.config_type}: {self.config_name}'

    @staticmethod
    def mask_secret(value):
        if not value:
            return '-'
        if len(value) <= 4:
            return '****'
        return f'****{value[-4:]}'

    @property
    def masked_api_key(self):
        return self.mask_secret(self.api_key)

    @property
    def masked_api_secret(self):
        return self.mask_secret(self.api_secret)

    @property
    def masked_password(self):
        return self.mask_secret(self.password)
