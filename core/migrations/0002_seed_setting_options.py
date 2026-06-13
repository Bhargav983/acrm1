from django.db import migrations


DEFAULT_SETTINGS = [
    ('Occupation', 'Business', 'Business', 10),
    ('Occupation', 'Service', 'Service', 20),
    ('Occupation', 'Professional', 'Professional', 30),
    ('Occupation', 'Student', 'Student', 40),
    ('Occupation', 'Homemaker', 'Homemaker', 50),
    ('Occupation', 'Retired', 'Retired', 60),
    ('Education', 'High School', 'High School', 10),
    ('Education', 'Graduate', 'Graduate', 20),
    ('Education', 'Post Graduate', 'Post Graduate', 30),
    ('Education', 'Doctorate', 'Doctorate', 40),
    ('Education', 'Professional Degree', 'Professional Degree', 50),
    ('Marital Status', 'single', 'Single', 10),
    ('Marital Status', 'married', 'Married', 20),
    ('Marital Status', 'divorced', 'Divorced', 30),
    ('Marital Status', 'widowed', 'Widowed', 40),
    ('Marital Status', 'not_specified', 'Not Specified', 50),
    ('Gender', 'male', 'Male', 10),
    ('Gender', 'female', 'Female', 20),
    ('Gender', 'other', 'Other', 30),
    ('Gender', 'not_specified', 'Not Specified', 40),
    ('Timezone', 'Asia/Kolkata', 'Asia/Kolkata', 10),
    ('Timezone', 'UTC', 'UTC', 20),
    ('Consultation Topic', 'career', 'Career', 10),
    ('Consultation Topic', 'marriage', 'Marriage', 20),
    ('Consultation Topic', 'health', 'Health', 30),
    ('Consultation Topic', 'finance', 'Finance', 40),
    ('Consultation Topic', 'education', 'Education', 50),
    ('Consultation Topic', 'spiritual_guidance', 'Spiritual Guidance', 60),
    ('Consultation Topic', 'general_consultation', 'General Consultation', 70),
    ('Knowledge Type', 'prediction', 'Prediction', 10),
    ('Knowledge Type', 'remedy', 'Remedy', 20),
    ('Knowledge Type', 'rule', 'Rule', 30),
    ('Knowledge Type', 'observation', 'Observation', 40),
    ('Knowledge Type', 'question', 'Question', 50),
    ('Knowledge Type', 'note', 'Note', 60),
    ('Section', 'nakshatra', 'Nakshatra', 10),
    ('Section', 'nakshatra_pada', 'Nakshatra Pada', 20),
    ('Section', 'dosha', 'Dosha', 30),
    ('Section', 'planet_in_house', 'Planet in House', 40),
    ('Section', 'planet_in_nakshatra', 'Planet in Nakshatra', 50),
    ('Section', 'planet_in_sign', 'Planet in Sign', 60),
    ('Section', 'arudha_lagna', 'Arudha Lagna', 70),
    ('Section', 'dasha', 'Dasha', 80),
    ('Section', 'transit', 'Transit', 90),
    ('Section', 'kp', 'KP', 100),
    ('Section', 'bnn', 'BNN', 110),
    ('Section', 'past_life', 'Past Life', 120),
    ('Section', 'remedy', 'Remedy', 130),
    ('Section', 'research', 'Research', 140),
    ('Section', 'case_study', 'Case Study', 150),
    ('Applies To Type', 'nakshatra', 'Nakshatra', 10),
    ('Applies To Type', 'pada', 'Pada', 20),
    ('Applies To Type', 'dosha', 'Dosha', 30),
    ('Applies To Type', 'planet', 'Planet', 40),
    ('Applies To Type', 'house', 'House', 50),
    ('Applies To Type', 'sign', 'Sign', 60),
    ('Applies To Type', 'planet_combination', 'Planet Combination', 70),
    ('Applies To Type', 'arudha', 'Arudha', 80),
    ('Applies To Type', 'dasha', 'Dasha', 90),
    ('Applies To Type', 'transit', 'Transit', 100),
    ('Applies To Type', 'general', 'General', 110),
    ('Related Factor', 'Career', 'Career', 10),
    ('Related Factor', 'Marriage', 'Marriage', 20),
    ('Related Factor', 'Health', 'Health', 30),
    ('Related Factor', 'Finance', 'Finance', 40),
    ('Related Factor', 'Education', 'Education', 50),
    ('Related Factor', 'Spirituality', 'Spirituality', 60),
    ('Related Factor', 'Family', 'Family', 70),
    ('Related Factor', 'Children', 'Children', 80),
    ('Related Factor', 'Business', 'Business', 90),
    ('Related Factor', 'Foreign Travel', 'Foreign Travel', 100),
    ('Tracking Type', 'prediction_verification', 'Prediction Verification', 10),
    ('Tracking Type', 'remedy_tracking', 'Remedy Tracking', 20),
    ('Tracking Type', 'research_answer', 'Research Answer', 30),
    ('Tracking Type', 'observation', 'Observation', 40),
    ('Verification Status', 'applies', 'Applies', 10),
    ('Verification Status', 'partially_applies', 'Partially Applies', 20),
    ('Verification Status', 'does_not_apply', 'Does Not Apply', 30),
    ('Verification Status', 'not_asked', 'Not Asked', 40),
    ('Remedy Status', 'suggested', 'Suggested', 10),
    ('Remedy Status', 'started', 'Started', 20),
    ('Remedy Status', 'in_progress', 'In Progress', 30),
    ('Remedy Status', 'completed', 'Completed', 40),
    ('Remedy Status', 'stopped', 'Stopped', 50),
    ('Research Status', 'answered', 'Answered', 10),
    ('Research Status', 'not_answered', 'Not Answered', 20),
    ('Research Status', 'needs_follow_up', 'Needs Follow-up', 30),
    ('Outcome', 'very_effective', 'Very Effective', 10),
    ('Outcome', 'effective', 'Effective', 20),
    ('Outcome', 'partial', 'Partial', 30),
    ('Outcome', 'no_effect', 'No Effect', 40),
    ('Outcome', 'negative_effect', 'Negative Effect', 50),
    ('Outcome', 'not_applicable', 'Not Applicable', 60),
    ('Role Type', 'Admin', 'Admin', 10),
    ('Role Type', 'Content Editor', 'Content Editor', 20),
    ('Role Type', 'Researcher', 'Researcher', 30),
    ('Role Type', 'Viewer', 'Viewer', 40),
]


def seed_settings(apps, schema_editor):
    SettingOption = apps.get_model('core', 'SettingOption')
    for setting_type, name, description, sort_order in DEFAULT_SETTINGS:
        SettingOption.objects.get_or_create(
            setting_type=setting_type,
            name=name,
            defaults={
                'description': description,
                'sort_order': sort_order,
                'is_active': True,
            },
        )


def remove_seed_settings(apps, schema_editor):
    SettingOption = apps.get_model('core', 'SettingOption')
    for setting_type, name, _description, _sort_order in DEFAULT_SETTINGS:
        SettingOption.objects.filter(setting_type=setting_type, name=name).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_settings, remove_seed_settings),
    ]
