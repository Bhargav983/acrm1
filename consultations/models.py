from django.conf import settings
from django.db import models


class ConsultationNote(models.Model):
    TOPIC_CHOICES = [
        ('career', 'Career'),
        ('marriage', 'Marriage'),
        ('health', 'Health'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('spiritual_guidance', 'Spiritual Guidance'),
        ('general_consultation', 'General Consultation'),
    ]

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='consultation_notes',
    )
    consultation_date = models.DateTimeField()
    topic = models.CharField(
        max_length=40,
        choices=TOPIC_CHOICES,
        default='general_consultation',
    )
    notes = models.TextField()
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='consultation_notes_created',
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='consultation_notes_updated',
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-consultation_date']

    def __str__(self):
        return f'{self.customer} - {self.get_topic_display()}'
