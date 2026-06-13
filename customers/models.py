from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Customer(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('not_specified', 'Not Specified'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('not_specified', 'Not Specified'),
    ]

    customer_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default='not_specified',
    )
    mobile_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    time_of_birth = models.TimeField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=150, blank=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    timezone = models.CharField(max_length=50, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        default='not_specified',
    )
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='customers_created',
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='customers_updated',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['customer_name']

    def __str__(self):
        return self.customer_name


class APIData(models.Model):
    DATA_SOURCE_CHOICES = [
        ('manual', 'Manual'),
        ('api', 'API'),
        ('imported_excel', 'Imported Excel'),
        ('imported_csv', 'Imported CSV'),
        ('imported_software', 'Imported Software'),
    ]

    API_TYPE_CHOICES = [
        ('birth_chart', 'Birth Chart'),
        ('dasha', 'Dasha'),
        ('transit', 'Transit'),
        ('kp', 'KP'),
        ('ashtakavarga', 'Ashtakavarga'),
        ('compatibility', 'Compatibility'),
        ('divisional_charts', 'Divisional Charts'),
        ('other', 'Other'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='api_data_records',
    )
    data_source = models.CharField(
        max_length=30,
        choices=DATA_SOURCE_CHOICES,
        default='manual',
    )
    api_provider = models.CharField(max_length=100, blank=True)
    api_name = models.CharField(max_length=100, blank=True)
    api_type = models.CharField(
        max_length=30,
        choices=API_TYPE_CHOICES,
        default='birth_chart',
    )
    request_date = models.DateTimeField(default=timezone.now)
    request_parameters = models.JSONField(default=dict, blank=True)
    lagna = models.CharField(max_length=100, blank=True)
    moon_sign = models.CharField(max_length=100, blank=True)
    sun_sign = models.CharField(max_length=100, blank=True)
    nakshatra = models.CharField(max_length=100, blank=True)
    pada = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    )
    current_mahadasha = models.CharField(max_length=100, blank=True)
    current_antardasha = models.CharField(max_length=100, blank=True)
    raw_api_response = models.JSONField(default=dict, blank=True)
    parsed_response = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-request_date']

    def __str__(self):
        return f'{self.customer} - {self.get_data_source_display()}'
