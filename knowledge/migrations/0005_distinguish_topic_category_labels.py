from django.db import migrations


DUPLICATE_TOPIC_RENAMES = [
    ('Remedy', 'Remedy Topic', 'General bucket for remedy-related knowledge records.'),
    ('Research', 'Research Topic', 'General bucket for research questions and findings.'),
    ('Case Study', 'Case Study Topic', 'General bucket for case study knowledge records.'),
    ('Past Life', 'Past Life Topic', 'General bucket for past-life observations and notes.'),
]


def distinguish_topic_category_labels(apps, schema_editor):
    Category = apps.get_model('knowledge', 'Category')
    for old_name, new_name, description in DUPLICATE_TOPIC_RENAMES:
        old_category = Category.objects.filter(category_name=old_name).first()
        if old_category and old_category.knowledge_records.exists():
            continue
        if old_category:
            old_category.category_name = new_name
            old_category.description = description
            old_category.is_active = True
            old_category.save(update_fields=['category_name', 'description', 'is_active'])
        else:
            Category.objects.get_or_create(
                category_name=new_name,
                defaults={
                    'description': description,
                    'is_active': True,
                },
            )


def restore_topic_category_labels(apps, schema_editor):
    Category = apps.get_model('knowledge', 'Category')
    for old_name, new_name, description in DUPLICATE_TOPIC_RENAMES:
        new_category = Category.objects.filter(category_name=new_name).first()
        if not new_category or new_category.knowledge_records.exists():
            continue
        new_category.category_name = old_name
        new_category.description = description
        new_category.is_active = True
        new_category.save(update_fields=['category_name', 'description', 'is_active'])


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0004_refine_default_category_dropdowns'),
    ]

    operations = [
        migrations.RunPython(
            distinguish_topic_category_labels,
            restore_topic_category_labels,
        ),
    ]
