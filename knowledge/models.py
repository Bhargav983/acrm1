from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category_name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class AstrologyKnowledge(models.Model):
    SYSTEM_CHOICES = [
        ('classical_astrology', 'Classical Astrology'),
        ('bnn', 'BNN'),
        ('kp', 'KP'),
        ('numerology', 'Numerology'),
        ('jaimini', 'Jaimini'),
    ]

    SECTION_CHOICES = [
        ('lagna', 'Lagna'),
        ('nakshatra', 'Nakshatra'),
        ('nakshatra_pada', 'Nakshatra Pada'),
        ('dosha', 'Dosha'),
        ('planet_in_house', 'Planet in House'),
        ('planet_in_nakshatra', 'Planet in Nakshatra'),
        ('planet_in_nakshatra_pada', 'Planet in Nakshatra Pada'),
        ('planet_in_sign', 'Planet in Sign'),
        ('house_lord_in_house', 'House Lord in House'),
        ('house_lord_in_sign', 'House Lord in Sign'),
        ('house_lord_in_nakshatra', 'House Lord in Nakshatra'),
        ('house_lord_in_nakshatra_pada', 'House Lord in Nakshatra Pada'),
        ('conjunction', 'Conjunction'),
        ('aspect', 'Aspect'),
        ('arudha_lagna', 'Arudha Lagna'),
        ('dasha', 'Dasha'),
        ('transit', 'Transit'),
        ('kp', 'KP'),
        ('house_signification', 'House Signification'),
        ('planet_significator', 'Planet Significator'),
        ('cuspal_sub_lord', 'Cuspal Sub Lord'),
        ('marriage_rule', 'Marriage Rule'),
        ('career_rule', 'Career Rule'),
        ('child_birth_rule', 'Child Birth Rule'),
        ('property_rule', 'Property Rule'),
        ('foreign_travel_rule', 'Foreign Travel Rule'),
        ('health_rule', 'Health Rule'),
        ('bnn', 'BNN'),
        ('bnn_rule', 'BNN Rule'),
        ('planet_activation_age', 'Planet Activation Age'),
        ('planet_combination', 'Planet Combination'),
        ('planet_chain', 'Planet Chain'),
        ('signification_transfer', 'Signification Transfer'),
        ('house_activation', 'House Activation'),
        ('event_timing', 'Event Timing'),
        ('marriage_pattern', 'Marriage Pattern'),
        ('career_pattern', 'Career Pattern'),
        ('spiritual_pattern', 'Spiritual Pattern'),
        ('karmic_pattern', 'Karmic Pattern'),
        ('life_path_number', 'Life Path Number'),
        ('destiny_number', 'Destiny Number'),
        ('soul_urge_number', 'Soul Urge Number'),
        ('personality_number', 'Personality Number'),
        ('name_number', 'Name Number'),
        ('personal_year_number', 'Personal Year Number'),
        ('compatibility', 'Compatibility'),
        ('financial_pattern', 'Financial Pattern'),
        ('relationship_pattern', 'Relationship Pattern'),
        ('health_pattern', 'Health Pattern'),
        ('atmakaraka', 'Atmakaraka'),
        ('amatyakaraka', 'Amatyakaraka'),
        ('darakaraka', 'Darakaraka'),
        ('karakamsha_lagna', 'Karakamsha Lagna'),
        ('swamsha', 'Swamsha'),
        ('pada_analysis', 'Pada Analysis'),
        ('chara_dasha', 'Chara Dasha'),
        ('upapada_lagna', 'Upapada Lagna'),
        ('career_indicators', 'Career Indicators'),
        ('marriage_indicators', 'Marriage Indicators'),
        ('spiritual_indicators', 'Spiritual Indicators'),
        ('past_life', 'Past Life'),
        ('remedy', 'Remedy'),
        ('research', 'Research'),
        ('case_study', 'Case Study'),
        ('yoga', 'Yoga'),
        ('age_activation', 'Age Activation'),
        ('kp_rule', 'KP Rule'),
        ('numerology_number', 'Numerology Number'),
        ('divisional_chart', 'Divisional Chart'),
    ]

    KNOWLEDGE_TYPE_CHOICES = [
        ('prediction', 'Prediction'),
        ('remedy', 'Remedy'),
        ('rule', 'Rule'),
        ('observation', 'Observation'),
        ('question', 'Question'),
        ('note', 'Note'),
    ]

    APPLIES_TO_TYPE_CHOICES = [
        ('nakshatra', 'Nakshatra'),
        ('pada', 'Pada'),
        ('dosha', 'Dosha'),
        ('planet', 'Planet'),
        ('house', 'House'),
        ('sign', 'Sign'),
        ('planet_combination', 'Planet Combination'),
        ('arudha', 'Arudha'),
        ('dasha', 'Dasha'),
        ('transit', 'Transit'),
        ('general', 'General'),
    ]

    NATURE_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
        ('remedy', 'Remedy'),
    ]

    CONFIDENCE_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('researching', 'Researching'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    system = models.CharField(
        max_length=40,
        choices=SYSTEM_CHOICES,
        default='classical_astrology',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='knowledge_records',
    )
    section = models.CharField(max_length=40, choices=SECTION_CHOICES)
    knowledge_type = models.CharField(
        max_length=30,
        choices=KNOWLEDGE_TYPE_CHOICES,
    )
    applies_to_type = models.CharField(
        max_length=40,
        choices=APPLIES_TO_TYPE_CHOICES,
        default='general',
    )
    applies_to_name = models.CharField(max_length=150, blank=True)
    applies_to_subtype = models.CharField(max_length=150, blank=True)
    related_factor = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    short_meaning = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    verification_question = models.TextField(blank=True)
    expected_result = models.TextField(blank=True)
    life_areas = models.CharField(max_length=255, blank=True)
    nature = models.CharField(
        max_length=20,
        choices=NATURE_CHOICES,
        default='neutral',
    )
    confidence_level = models.CharField(
        max_length=20,
        choices=CONFIDENCE_LEVEL_CHOICES,
        default='medium',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='knowledge_created',
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='knowledge_updated',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class HypothesisQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('yes_no', 'Yes/No'),
        ('rating', 'Rating'),
        ('text', 'Text'),
        ('single_choice', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice'),
    ]

    hypothesis = models.ForeignKey(
        AstrologyKnowledge,
        on_delete=models.CASCADE,
        related_name='questions',
    )
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=30,
        choices=QUESTION_TYPE_CHOICES,
        default='yes_no',
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.question_text


class CustomerResearchAnswer(models.Model):
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='research_answers',
    )
    hypothesis = models.ForeignKey(
        AstrologyKnowledge,
        on_delete=models.CASCADE,
        related_name='research_answers',
    )
    question = models.ForeignKey(
        HypothesisQuestion,
        on_delete=models.CASCADE,
        related_name='customer_answers',
    )
    answer_text = models.TextField(blank=True)
    answer_value = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    answered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='research_answers_recorded',
        null=True,
        blank=True,
    )
    answered_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-answered_date', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'hypothesis', 'question'],
                name='unique_customer_hypothesis_question_answer',
            ),
        ]

    def __str__(self):
        return f'{self.customer} - {self.question}'


class CustomerKnowledgeTracking(models.Model):
    TRACKING_TYPE_CHOICES = [
        ('prediction_verification', 'Prediction Verification'),
        ('remedy_tracking', 'Remedy Tracking'),
        ('research_answer', 'Research Answer'),
        ('observation', 'Observation'),
    ]

    STATUS_CHOICES = [
        ('applies', 'Applies'),
        ('partially_applies', 'Partially Applies'),
        ('does_not_apply', 'Does Not Apply'),
        ('not_asked', 'Not Asked'),
        ('suggested', 'Suggested'),
        ('started', 'Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('stopped', 'Stopped'),
        ('answered', 'Answered'),
        ('not_answered', 'Not Answered'),
        ('needs_follow_up', 'Needs Follow-up'),
    ]

    OUTCOME_CHOICES = [
        ('very_effective', 'Very Effective'),
        ('effective', 'Effective'),
        ('partial', 'Partial'),
        ('no_effect', 'No Effect'),
        ('negative_effect', 'Negative Effect'),
        ('not_applicable', 'Not Applicable'),
    ]

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='knowledge_tracking_records',
    )
    knowledge = models.ForeignKey(
        AstrologyKnowledge,
        on_delete=models.CASCADE,
        related_name='customer_tracking_records',
    )
    tracking_type = models.CharField(
        max_length=40,
        choices=TRACKING_TYPE_CHOICES,
    )
    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default='not_asked',
    )
    customer_feedback = models.TextField(blank=True)
    researcher_notes = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    effectiveness_rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    outcome = models.CharField(
        max_length=30,
        choices=OUTCOME_CHOICES,
        blank=True,
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='verified_tracking_records',
        null=True,
        blank=True,
    )
    verified_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.customer} - {self.knowledge}'
