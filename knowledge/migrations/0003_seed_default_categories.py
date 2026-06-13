from django.db import migrations


DEFAULT_CATEGORIES = [
    ('Nakshatra', 'Research related to nakshatras.'),
    ('Nakshatra Pada', 'Research related to nakshatra padas.'),
    ('Dosha', 'Dosha observations, rules, and related research.'),
    ('Remedy', 'Remedies and remedy tracking knowledge.'),
    ('KP', 'KP astrology rules and observations.'),
    ('BNN', 'BNN astrology rules and observations.'),
    ('Arudha', 'Arudha and Jaimini-related observations.'),
    ('Dasha', 'Dasha period rules and observations.'),
    ('Transit', 'Transit rules and observations.'),
    ('Planet in House', 'Planet-in-house rules and observations.'),
    ('Planet in Nakshatra', 'Planet-in-nakshatra rules and observations.'),
    ('Planet in Sign', 'Planet-in-sign rules and observations.'),
    ('Past Life', 'Past life observations and research notes.'),
    ('Research', 'Research questions, findings, and open observations.'),
    ('Case Study', 'Case study notes and customer pattern observations.'),
    ('Career', 'Career-related predictions, rules, and observations.'),
    ('Marriage', 'Marriage-related predictions, rules, and observations.'),
    ('Health', 'Health-related predictions, rules, and observations.'),
    ('Finance', 'Finance-related predictions, rules, and observations.'),
    ('Spiritual', 'Spirituality-related predictions, remedies, and observations.'),
    ('Personality', 'Personality-related predictions and observations.'),
]


def seed_default_categories(apps, schema_editor):
    Category = apps.get_model('knowledge', 'Category')
    for category_name, description in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(
            category_name=category_name,
            defaults={
                'description': description,
                'is_active': True,
            },
        )


def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('knowledge', 'Category')
    names = [category_name for category_name, _description in DEFAULT_CATEGORIES]
    Category.objects.filter(
        category_name__in=names,
        knowledge_records__isnull=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0002_customerknowledgetracking_is_active'),
    ]

    operations = [
        migrations.RunPython(seed_default_categories, remove_default_categories),
    ]
