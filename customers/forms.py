from django import forms

from core.settings_utils import get_setting_choices

from .models import APIData, Customer


ZODIAC_SIGN_CHOICES = [
    ('Aries', 'Aries'),
    ('Taurus', 'Taurus'),
    ('Gemini', 'Gemini'),
    ('Cancer', 'Cancer'),
    ('Leo', 'Leo'),
    ('Virgo', 'Virgo'),
    ('Libra', 'Libra'),
    ('Scorpio', 'Scorpio'),
    ('Sagittarius', 'Sagittarius'),
    ('Capricorn', 'Capricorn'),
    ('Aquarius', 'Aquarius'),
    ('Pisces', 'Pisces'),
]

NAKSHATRA_CHOICES = [
    ('Ashwini', 'Ashwini'),
    ('Bharani', 'Bharani'),
    ('Krittika', 'Krittika'),
    ('Rohini', 'Rohini'),
    ('Mrigashira', 'Mrigashira'),
    ('Ardra', 'Ardra'),
    ('Punarvasu', 'Punarvasu'),
    ('Pushya', 'Pushya'),
    ('Ashlesha', 'Ashlesha'),
    ('Magha', 'Magha'),
    ('Purva Phalguni', 'Purva Phalguni'),
    ('Uttara Phalguni', 'Uttara Phalguni'),
    ('Hasta', 'Hasta'),
    ('Chitra', 'Chitra'),
    ('Swati', 'Swati'),
    ('Vishakha', 'Vishakha'),
    ('Anuradha', 'Anuradha'),
    ('Jyeshtha', 'Jyeshtha'),
    ('Mula', 'Mula'),
    ('Purva Ashadha', 'Purva Ashadha'),
    ('Uttara Ashadha', 'Uttara Ashadha'),
    ('Shravana', 'Shravana'),
    ('Dhanishta', 'Dhanishta'),
    ('Shatabhisha', 'Shatabhisha'),
    ('Purva Bhadrapada', 'Purva Bhadrapada'),
    ('Uttara Bhadrapada', 'Uttara Bhadrapada'),
    ('Revati', 'Revati'),
]

PADA_CHOICES = [
    (1, 'Pada 1'),
    (2, 'Pada 2'),
    (3, 'Pada 3'),
    (4, 'Pada 4'),
]

DASHA_LORD_CHOICES = [
    ('Ketu', 'Ketu'),
    ('Venus', 'Venus'),
    ('Sun', 'Sun'),
    ('Moon', 'Moon'),
    ('Mars', 'Mars'),
    ('Rahu', 'Rahu'),
    ('Jupiter', 'Jupiter'),
    ('Saturn', 'Saturn'),
    ('Mercury', 'Mercury'),
]

PLANET_CHOICES = [
    ('Sun', 'Sun'),
    ('Moon', 'Moon'),
    ('Mars', 'Mars'),
    ('Mercury', 'Mercury'),
    ('Jupiter', 'Jupiter'),
    ('Venus', 'Venus'),
    ('Saturn', 'Saturn'),
    ('Rahu', 'Rahu'),
    ('Ketu', 'Ketu'),
]

HOUSE_CHOICES = [
    ('1st House', '1st House'),
    ('2nd House', '2nd House'),
    ('3rd House', '3rd House'),
    ('4th House', '4th House'),
    ('5th House', '5th House'),
    ('6th House', '6th House'),
    ('7th House', '7th House'),
    ('8th House', '8th House'),
    ('9th House', '9th House'),
    ('10th House', '10th House'),
    ('11th House', '11th House'),
    ('12th House', '12th House'),
]

ASTROLOGY_PLANETS = [
    ('sun', 'Sun'),
    ('moon', 'Moon'),
    ('mars', 'Mars'),
    ('mercury', 'Mercury'),
    ('jupiter', 'Jupiter'),
    ('venus', 'Venus'),
    ('saturn', 'Saturn'),
    ('rahu', 'Rahu'),
    ('ketu', 'Ketu'),
]

HOUSE_NUMBERS = [
    (1, '1st House'),
    (2, '2nd House'),
    (3, '3rd House'),
    (4, '4th House'),
    (5, '5th House'),
    (6, '6th House'),
    (7, '7th House'),
    (8, '8th House'),
    (9, '9th House'),
    (10, '10th House'),
    (11, '11th House'),
    (12, '12th House'),
]

SIGN_LORDS = {
    'Aries': 'Mars',
    'Taurus': 'Venus',
    'Gemini': 'Mercury',
    'Cancer': 'Moon',
    'Leo': 'Sun',
    'Virgo': 'Mercury',
    'Libra': 'Venus',
    'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter',
    'Capricorn': 'Saturn',
    'Aquarius': 'Saturn',
    'Pisces': 'Jupiter',
}

NAKSHATRA_LORDS = {
    'Ashwini': 'Ketu',
    'Bharani': 'Venus',
    'Krittika': 'Sun',
    'Rohini': 'Moon',
    'Mrigashira': 'Mars',
    'Ardra': 'Rahu',
    'Punarvasu': 'Jupiter',
    'Pushya': 'Saturn',
    'Ashlesha': 'Mercury',
    'Magha': 'Ketu',
    'Purva Phalguni': 'Venus',
    'Uttara Phalguni': 'Sun',
    'Hasta': 'Moon',
    'Chitra': 'Mars',
    'Swati': 'Rahu',
    'Vishakha': 'Jupiter',
    'Anuradha': 'Saturn',
    'Jyeshtha': 'Mercury',
    'Mula': 'Ketu',
    'Purva Ashadha': 'Venus',
    'Uttara Ashadha': 'Sun',
    'Shravana': 'Moon',
    'Dhanishta': 'Mars',
    'Shatabhisha': 'Rahu',
    'Purva Bhadrapada': 'Jupiter',
    'Uttara Bhadrapada': 'Saturn',
    'Revati': 'Mercury',
}

PLANET_RELATIONSHIPS = {
    'Sun': {
        'friends': ['Moon', 'Mars', 'Jupiter'],
        'enemies': ['Venus', 'Saturn', 'Rahu', 'Ketu'],
    },
    'Moon': {
        'friends': ['Sun', 'Mercury'],
        'enemies': [],
    },
    'Mars': {
        'friends': ['Sun', 'Moon', 'Jupiter'],
        'enemies': ['Mercury', 'Rahu', 'Ketu'],
    },
    'Mercury': {
        'friends': ['Sun', 'Venus'],
        'enemies': ['Moon'],
    },
    'Jupiter': {
        'friends': ['Sun', 'Moon', 'Mars'],
        'enemies': ['Mercury', 'Venus', 'Rahu', 'Ketu'],
    },
    'Venus': {
        'friends': ['Mercury', 'Saturn'],
        'enemies': ['Sun', 'Moon'],
    },
    'Saturn': {
        'friends': ['Mercury', 'Venus'],
        'enemies': ['Sun', 'Moon', 'Mars'],
    },
    'Rahu': {
        'friends': ['Mercury', 'Venus', 'Saturn'],
        'enemies': ['Sun', 'Moon', 'Mars'],
    },
    'Ketu': {
        'friends': ['Mars', 'Venus', 'Saturn'],
        'enemies': ['Sun', 'Moon'],
    },
}


def choices_with_blank(choices, current_value=None):
    prepared = list(choices)
    values = [value for value, _label in prepared]
    if current_value and current_value not in values:
        prepared.append((current_value, current_value))
    return [('', '---------')] + prepared


def destination_sign_from_house(source_sign, destination_house):
    signs = [value for value, _label in ZODIAC_SIGN_CHOICES]
    if source_sign not in signs or not destination_house:
        return ''
    try:
        house_number = int(str(destination_house).split()[0][:-2])
    except (TypeError, ValueError):
        return ''
    return signs[(signs.index(source_sign) + house_number - 1) % len(signs)]


def sign_from_lagna_house(lagna, house):
    return destination_sign_from_house(lagna, house)


def planet_relationship(planet, other_planet):
    if not planet or not other_planet:
        return ''
    if planet == other_planet:
        return 'Own'
    relationship = PLANET_RELATIONSHIPS.get(planet, {})
    if other_planet in relationship.get('friends', []):
        return 'Friend'
    if other_planet in relationship.get('enemies', []):
        return 'Enemy'
    return 'Neutral'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_name',
            'gender',
            'mobile_number',
            'email',
            'date_of_birth',
            'time_of_birth',
            'place_of_birth',
            'latitude',
            'longitude',
            'timezone',
            'occupation',
            'education',
            'marital_status',
            'notes',
            'is_active',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'time_of_birth': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = get_setting_choices(
            'Gender',
            fallback_choices=Customer.GENDER_CHOICES,
            include_blank=False,
            current_value=self.instance.gender if self.instance.pk else None,
        )
        self.fields['gender'].widget.choices = self.fields['gender'].choices
        self.fields['occupation'].widget = forms.Select()
        self.fields['occupation'].choices = get_setting_choices(
            'Occupation',
            current_value=self.instance.occupation if self.instance.pk else None,
        )
        self.fields['occupation'].widget.choices = self.fields['occupation'].choices
        self.fields['education'].widget = forms.Select()
        self.fields['education'].choices = get_setting_choices(
            'Education',
            current_value=self.instance.education if self.instance.pk else None,
        )
        self.fields['education'].widget.choices = self.fields['education'].choices
        self.fields['marital_status'].choices = get_setting_choices(
            'Marital Status',
            fallback_choices=Customer.MARITAL_STATUS_CHOICES,
            include_blank=False,
            current_value=self.instance.marital_status if self.instance.pk else None,
        )
        self.fields['marital_status'].widget.choices = self.fields['marital_status'].choices
        self.fields['timezone'].widget = forms.Select()
        self.fields['timezone'].choices = get_setting_choices(
            'Timezone',
            current_value=self.instance.timezone if self.instance.pk else None,
        )
        self.fields['timezone'].widget.choices = self.fields['timezone'].choices
        for field in self.fields.values():
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class


class APIDataForm(forms.ModelForm):
    class Meta:
        model = APIData
        fields = [
            'customer',
            'data_source',
            'lagna',
            'moon_sign',
            'sun_sign',
            'nakshatra',
            'pada',
            'current_mahadasha',
            'current_antardasha',
            'notes',
            'is_active',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(is_active=True)
        self.manual_field_names = []
        self.planet_sign_rows = []
        self.planet_house_rows = []
        self.planet_nakshatra_rows = []
        self.house_lord_rows = []
        self.add_manual_astrology_fields()

        manual_entries = {}
        if self.instance and self.instance.pk and isinstance(self.instance.parsed_response, dict):
            manual_entries = self.instance.parsed_response.get('manual_entries', {})
        for field_name, value in manual_entries.items():
            if field_name in self.fields:
                self.fields[field_name].initial = value

        sign_fields = ['lagna', 'moon_sign', 'sun_sign']
        for field_name in sign_fields:
            self.fields[field_name].widget = forms.Select()
            current_value = getattr(self.instance, field_name, None) if self.instance.pk else None
            self.fields[field_name].choices = choices_with_blank(
                ZODIAC_SIGN_CHOICES,
                current_value=current_value,
            )
            self.fields[field_name].widget.choices = self.fields[field_name].choices

        self.fields['nakshatra'].widget = forms.Select()
        self.fields['nakshatra'].choices = choices_with_blank(
            NAKSHATRA_CHOICES,
            current_value=self.instance.nakshatra if self.instance.pk else None,
        )
        self.fields['nakshatra'].widget.choices = self.fields['nakshatra'].choices

        self.fields['pada'].widget = forms.Select()
        self.fields['pada'].choices = choices_with_blank(
            PADA_CHOICES,
            current_value=self.instance.pada if self.instance.pk else None,
        )
        self.fields['pada'].widget.choices = self.fields['pada'].choices

        dasha_fields = ['current_mahadasha', 'current_antardasha']
        for field_name in dasha_fields:
            self.fields[field_name].widget = forms.Select()
            current_value = getattr(self.instance, field_name, None) if self.instance.pk else None
            self.fields[field_name].choices = choices_with_blank(
                DASHA_LORD_CHOICES,
                current_value=current_value,
            )
            self.fields[field_name].widget.choices = self.fields[field_name].choices

        for field in self.fields.values():
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class

    def add_manual_astrology_fields(self):
        for slug, label in ASTROLOGY_PLANETS:
            sign_field = f'planet_sign_{slug}'
            sign_lord_field = f'planet_sign_{slug}_lord'
            sign_relationship_field = f'planet_sign_{slug}_relationship'
            self.fields[sign_field] = forms.ChoiceField(
                choices=choices_with_blank(ZODIAC_SIGN_CHOICES),
                required=False,
                label=f'{label} Sign',
            )
            self.fields[sign_lord_field] = forms.CharField(
                required=False,
                label='Sign Lord',
                widget=forms.TextInput(attrs={'readonly': 'readonly'}),
            )
            self.fields[sign_relationship_field] = forms.CharField(
                required=False,
                label='Relationship',
                widget=forms.TextInput(attrs={'readonly': 'readonly'}),
            )
            self.manual_field_names.extend(
                [sign_field, sign_lord_field, sign_relationship_field]
            )
            self.planet_sign_rows.append(
                {
                    'planet': label,
                    'sign': self[sign_field],
                    'lord': self[sign_lord_field],
                    'relationship': self[sign_relationship_field],
                }
            )

            house_field = f'planet_house_{slug}'
            self.fields[house_field] = forms.ChoiceField(
                choices=choices_with_blank(HOUSE_CHOICES),
                required=False,
                label=f'{label} House',
            )
            self.manual_field_names.append(house_field)
            self.planet_house_rows.append(
                {
                    'planet': label,
                    'house': self[house_field],
                }
            )

            nakshatra_field = f'planet_nakshatra_{slug}'
            pada_field = f'planet_nakshatra_{slug}_pada'
            owner_field = f'planet_nakshatra_{slug}_owner'
            relationship_field = f'planet_nakshatra_{slug}_relationship'
            self.fields[nakshatra_field] = forms.ChoiceField(
                choices=choices_with_blank(NAKSHATRA_CHOICES),
                required=False,
                label=f'{label} Nakshatra',
            )
            self.fields[pada_field] = forms.ChoiceField(
                choices=choices_with_blank(PADA_CHOICES),
                required=False,
                label=f'{label} Pada',
            )
            self.fields[owner_field] = forms.CharField(
                required=False,
                label='Owner',
                widget=forms.TextInput(attrs={'readonly': 'readonly'}),
            )
            self.fields[relationship_field] = forms.CharField(
                required=False,
                label='Relationship',
                widget=forms.TextInput(attrs={'readonly': 'readonly'}),
            )
            self.manual_field_names.extend(
                [nakshatra_field, pada_field, owner_field, relationship_field]
            )
            self.planet_nakshatra_rows.append(
                {
                    'planet': label,
                    'nakshatra': self[nakshatra_field],
                    'pada': self[pada_field],
                    'owner': self[owner_field],
                    'relationship': self[relationship_field],
                }
            )

        for house_number, house_label in HOUSE_NUMBERS:
            source_sign_field = f'house_lord_{house_number}_source_sign'
            lord_planet_field = f'house_lord_{house_number}_lord_planet'
            destination_house_field = f'house_lord_{house_number}_destination_house'
            destination_sign_field = f'house_lord_{house_number}_destination_sign'
            relationship_field = f'house_lord_{house_number}_relationship'
            self.fields[source_sign_field] = forms.ChoiceField(
                choices=choices_with_blank(ZODIAC_SIGN_CHOICES),
                required=False,
                label='Sign',
            )
            self.fields[lord_planet_field] = forms.CharField(
                required=False,
                label='Lord',
                widget=forms.TextInput(attrs={'readonly': 'readonly'}),
            )
            self.fields[destination_house_field] = forms.ChoiceField(
                choices=choices_with_blank(HOUSE_CHOICES),
                required=False,
                label='Goes To House',
            )
            self.fields[destination_sign_field] = forms.ChoiceField(
                choices=choices_with_blank(ZODIAC_SIGN_CHOICES),
                required=False,
                label='Destination Sign',
            )
            self.fields[relationship_field] = forms.CharField(
                required=False,
                label='Relationship',
                widget=forms.TextInput(attrs={'readonly': 'readonly'}),
            )
            self.manual_field_names.extend(
                [
                    source_sign_field,
                    lord_planet_field,
                    destination_house_field,
                    destination_sign_field,
                    relationship_field,
                ]
            )
            self.house_lord_rows.append(
                {
                    'house': house_label,
                    'source_sign': self[source_sign_field],
                    'lord_planet': self[lord_planet_field],
                    'destination_house': self[destination_house_field],
                    'destination_sign': self[destination_sign_field],
                    'relationship': self[relationship_field],
                }
            )

    def clean(self):
        cleaned_data = super().clean()
        for slug, planet in ASTROLOGY_PLANETS:
            sign_field = f'planet_sign_{slug}'
            sign_lord_field = f'planet_sign_{slug}_lord'
            sign_relationship_field = f'planet_sign_{slug}_relationship'
            sign = cleaned_data.get(sign_field)
            sign_lord = SIGN_LORDS.get(sign, '')
            cleaned_data[sign_lord_field] = sign_lord
            cleaned_data[sign_relationship_field] = planet_relationship(planet, sign_lord)

        for house_number, _house_label in HOUSE_NUMBERS:
            source_sign_field = f'house_lord_{house_number}_source_sign'
            lord_planet_field = f'house_lord_{house_number}_lord_planet'
            destination_house_field = f'house_lord_{house_number}_destination_house'
            destination_sign_field = f'house_lord_{house_number}_destination_sign'
            relationship_field = f'house_lord_{house_number}_relationship'
            source_sign = cleaned_data.get(source_sign_field)
            destination_house = cleaned_data.get(destination_house_field)
            if source_sign:
                cleaned_data[lord_planet_field] = SIGN_LORDS.get(source_sign, '')
            if source_sign and destination_house:
                cleaned_data[destination_sign_field] = destination_sign_from_house(
                    source_sign,
                    destination_house,
                )
            cleaned_data[relationship_field] = planet_relationship(
                cleaned_data.get(lord_planet_field),
                SIGN_LORDS.get(cleaned_data.get(destination_sign_field), ''),
            )
        for slug, planet in ASTROLOGY_PLANETS:
            nakshatra_field = f'planet_nakshatra_{slug}'
            owner_field = f'planet_nakshatra_{slug}_owner'
            relationship_field = f'planet_nakshatra_{slug}_relationship'
            nakshatra = cleaned_data.get(nakshatra_field)
            owner = NAKSHATRA_LORDS.get(nakshatra, '')
            cleaned_data[owner_field] = owner
            cleaned_data[relationship_field] = planet_relationship(planet, owner)
        return cleaned_data

    def save(self, commit=True):
        api_data = super().save(commit=False)
        parsed_response = api_data.parsed_response if isinstance(api_data.parsed_response, dict) else {}
        manual_entries = {}
        for field_name in self.manual_field_names:
            value = self.cleaned_data.get(field_name)
            if value:
                manual_entries[field_name] = value
        if manual_entries:
            parsed_response['manual_entries'] = manual_entries
        else:
            parsed_response.pop('manual_entries', None)
        api_data.parsed_response = parsed_response
        if commit:
            api_data.save()
            self.save_m2m()
        return api_data
