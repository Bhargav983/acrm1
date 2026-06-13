from .models import SettingOption


def get_setting_choices(
    setting_type,
    fallback_choices=None,
    include_blank=True,
    current_value=None,
):
    options = SettingOption.objects.filter(
        setting_type=setting_type,
        is_active=True,
    ).order_by('sort_order', 'name')
    choices = [(option.name, option.description or option.name) for option in options]

    if fallback_choices:
        existing_values = [value for value, _label in choices]
        choices += [
            (value, label)
            for value, label in fallback_choices
            if value not in existing_values
        ]

    if current_value and current_value not in [value for value, _label in choices]:
        choices.append((current_value, current_value))

    if include_blank:
        return [('', '---------')] + choices
    return choices
