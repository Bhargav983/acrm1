from django.db import migrations


SECTION_LIKE_CATEGORIES = [
    'Nakshatra',
    'Nakshatra Pada',
    'Dosha',
    'KP',
    'BNN',
    'Arudha',
    'Dasha',
    'Transit',
    'Planet in House',
    'Planet in Nakshatra',
    'Planet in Sign',
]

TOPIC_CATEGORIES = [
    ('Education', 'Education-related predictions, rules, and observations.'),
    ('Family', 'Family-related predictions, rules, and observations.'),
    ('Children', 'Children-related predictions, rules, and observations.'),
    ('Business', 'Business-related predictions, rules, and observations.'),
    ('Foreign Travel', 'Foreign travel-related predictions, rules, and observations.'),
]


def refine_default_categories(apps, schema_editor):
    Category = apps.get_model('knowledge', 'Category')
    Category.objects.filter(
        category_name__in=SECTION_LIKE_CATEGORIES,
        knowledge_records__isnull=True,
    ).update(is_active=False)

    for category_name, description in TOPIC_CATEGORIES:
        Category.objects.get_or_create(
            category_name=category_name,
            defaults={
                'description': description,
                'is_active': True,
            },
        )


def restore_section_like_categories(apps, schema_editor):
    Category = apps.get_model('knowledge', 'Category')
    Category.objects.filter(category_name__in=SECTION_LIKE_CATEGORIES).update(
        is_active=True,
    )
    Category.objects.filter(
        category_name__in=[name for name, _description in TOPIC_CATEGORIES],
        knowledge_records__isnull=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0003_seed_default_categories'),
    ]

    operations = [
        migrations.RunPython(refine_default_categories, restore_section_like_categories),
    ]
