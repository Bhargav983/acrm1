from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, F, Q
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render

from consultations.models import ConsultationNote
from core.forms import AppConfigForm, SettingOptionForm
from core.models import AppConfig, SettingOption
from customers.models import Customer
from knowledge.models import AstrologyKnowledge, CustomerKnowledgeTracking


@login_required
def dashboard(request):
    today = timezone.localdate()
    verifications = CustomerKnowledgeTracking.objects.select_related(
        'customer',
        'knowledge',
    )
    consultations = ConsultationNote.objects.select_related('customer')

    context = {
        'total_customers': Customer.objects.count(),
        'total_knowledge_records': AstrologyKnowledge.objects.count(),
        'total_verifications': verifications.count(),
        'active_remedies': verifications.filter(
            tracking_type='remedy_tracking',
            is_active=True,
        ).count(),
        'todays_followups': consultations.filter(
            follow_up_required=True,
            follow_up_date=today,
        ).count(),
        'recent_customers': Customer.objects.order_by('-created_at')[:5],
        'recent_consultations': consultations.order_by('-consultation_date')[:5],
        'today': today,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def reports(request):
    occupation_filter = request.GET.get('occupation', '').strip()
    education_filter = request.GET.get('education', '').strip()
    marital_status_filter = request.GET.get('marital_status', '').strip()
    consultation_date_filter = request.GET.get('consultation_date', '').strip()

    customers = Customer.objects.all()
    if occupation_filter:
        customers = customers.filter(occupation__icontains=occupation_filter)
    if education_filter:
        customers = customers.filter(education__icontains=education_filter)
    if marital_status_filter:
        customers = customers.filter(marital_status=marital_status_filter)

    consultations = ConsultationNote.objects.select_related('customer')
    if consultation_date_filter:
        consultations = consultations.filter(
            consultation_date__date=consultation_date_filter
        )

    knowledge_records = AstrologyKnowledge.objects.select_related('category')
    verifications = CustomerKnowledgeTracking.objects.select_related(
        'customer',
        'knowledge',
    )
    remedy_records = verifications.filter(tracking_type='remedy_tracking')
    today = timezone.localdate()

    context = {
        'page_title': 'Reports',
        'occupation_filter': occupation_filter,
        'education_filter': education_filter,
        'marital_status_filter': marital_status_filter,
        'marital_status_choices': Customer.MARITAL_STATUS_CHOICES,
        'consultation_date_filter': consultation_date_filter,
        'total_customers': customers.count(),
        'active_customers': customers.filter(is_active=True).count(),
        'recent_customers': customers.order_by('-created_at')[:10],
        'total_knowledge_records': knowledge_records.count(),
        'knowledge_by_category': knowledge_records.values(
            label=F('category__category_name')
        ).annotate(total=Count('id')).order_by('label'),
        'knowledge_by_section': knowledge_records.values(
            label=F('section')
        ).annotate(total=Count('id')).order_by('label'),
        'knowledge_by_type': knowledge_records.values(
            label=F('knowledge_type')
        ).annotate(total=Count('id')).order_by('label'),
        'total_verifications': verifications.count(),
        'verifications_by_type': verifications.values(
            label=F('tracking_type')
        ).annotate(total=Count('id')).order_by('label'),
        'verifications_by_status': verifications.values(
            label=F('status')
        ).annotate(total=Count('id')).order_by('label'),
        'verifications_by_outcome': verifications.exclude(outcome='').values(
            label=F('outcome')
        ).annotate(total=Count('id')).order_by('label'),
        'recent_verifications': verifications.order_by('-created_at')[:10],
        'total_remedies': remedy_records.count(),
        'remedies_by_status': remedy_records.values(
            label=F('status')
        ).annotate(total=Count('id')).order_by('label'),
        'remedies_by_outcome': remedy_records.exclude(outcome='').values(
            label=F('outcome')
        ).annotate(total=Count('id')).order_by('label'),
        'average_remedy_rating': remedy_records.aggregate(
            average=Avg('effectiveness_rating')
        )['average'],
        'recent_remedies': remedy_records.order_by('-created_at')[:10],
        'total_consultations': consultations.count(),
        'followups_required': consultations.filter(follow_up_required=True).count(),
        'upcoming_followups': consultations.filter(
            follow_up_required=True,
            follow_up_date__gte=today,
        ).order_by('follow_up_date')[:10],
        'recent_consultations': consultations.order_by('-consultation_date')[:10],
    }
    return render(request, 'core/reports.html', context)


@login_required
def settings_list(request):
    search_query = request.GET.get('q', '').strip()
    setting_type_filter = request.GET.get('setting_type', '')
    status_filter = request.GET.get('status', 'active')
    settings = SettingOption.objects.select_related('created_by', 'updated_by')

    if status_filter == 'active':
        settings = settings.filter(is_active=True)
    elif status_filter == 'inactive':
        settings = settings.filter(is_active=False)

    if setting_type_filter:
        settings = settings.filter(setting_type=setting_type_filter)

    if search_query:
        settings = settings.filter(name__icontains=search_query)

    return render(
        request,
        'core/settings_list.html',
        {
            'page_title': 'Settings',
            'settings': settings,
            'setting_type_choices': SettingOption.SETTING_TYPE_CHOICES,
            'search_query': search_query,
            'setting_type_filter': setting_type_filter,
            'status_filter': status_filter,
        },
    )


@login_required
def settings_detail(request, pk):
    setting = get_object_or_404(SettingOption, pk=pk)
    return render(
        request,
        'core/settings_detail.html',
        {
            'page_title': setting.description or setting.name,
            'setting': setting,
        },
    )


@login_required
def settings_create(request):
    if request.method == 'POST':
        form = SettingOptionForm(request.POST)
        if form.is_valid():
            setting = form.save(commit=False)
            setting.created_by = request.user
            setting.updated_by = request.user
            setting.save()
            messages.success(request, 'Setting option created successfully.')
            return redirect('core:settings_detail', pk=setting.pk)
    else:
        form = SettingOptionForm()

    return render(
        request,
        'core/settings_form.html',
        {
            'page_title': 'Add Setting',
            'form': form,
            'submit_label': 'Create Setting',
        },
    )


@login_required
def settings_update(request, pk):
    setting = get_object_or_404(SettingOption, pk=pk)
    if request.method == 'POST':
        form = SettingOptionForm(request.POST, instance=setting)
        if form.is_valid():
            setting = form.save(commit=False)
            setting.updated_by = request.user
            setting.save()
            messages.success(request, 'Setting option updated successfully.')
            return redirect('core:settings_detail', pk=setting.pk)
    else:
        form = SettingOptionForm(instance=setting)

    return render(
        request,
        'core/settings_form.html',
        {
            'page_title': 'Edit Setting',
            'form': form,
            'setting': setting,
            'submit_label': 'Save Changes',
        },
    )


@login_required
def settings_deactivate(request, pk):
    setting = get_object_or_404(SettingOption, pk=pk)
    if request.method == 'POST':
        setting.is_active = False
        setting.updated_by = request.user
        setting.save(update_fields=['is_active', 'updated_by', 'updated_at'])
        messages.success(request, 'Setting option deactivated successfully.')
        return redirect('core:settings_list')

    return render(
        request,
        'core/settings_confirm_deactivate.html',
        {
            'page_title': 'Deactivate Setting',
            'setting': setting,
        },
    )


@login_required
def config_list(request):
    search_query = request.GET.get('q', '').strip()
    config_type_filter = request.GET.get('config_type', '')
    status_filter = request.GET.get('status', 'active')
    configs = AppConfig.objects.select_related('created_by', 'updated_by')

    if status_filter == 'active':
        configs = configs.filter(is_active=True)
    elif status_filter == 'inactive':
        configs = configs.filter(is_active=False)

    if config_type_filter:
        configs = configs.filter(config_type=config_type_filter)

    if search_query:
        configs = configs.filter(
            Q(config_name__icontains=search_query)
            | Q(provider_name__icontains=search_query)
            | Q(sender_email__icontains=search_query)
            | Q(smtp_host__icontains=search_query)
        )

    return render(
        request,
        'core/config_list.html',
        {
            'page_title': 'Configurations',
            'configs': configs,
            'config_type_choices': AppConfig.CONFIG_TYPE_CHOICES,
            'search_query': search_query,
            'config_type_filter': config_type_filter,
            'status_filter': status_filter,
        },
    )


@login_required
def config_detail(request, pk):
    config = get_object_or_404(AppConfig, pk=pk)
    return render(
        request,
        'core/config_detail.html',
        {
            'page_title': config.config_name,
            'config': config,
        },
    )


@login_required
def config_create(request):
    if request.method == 'POST':
        form = AppConfigForm(request.POST)
        if form.is_valid():
            config = form.save(commit=False)
            config.created_by = request.user
            config.updated_by = request.user
            config.save()
            messages.success(request, 'Configuration created successfully.')
            return redirect('core:config_detail', pk=config.pk)
    else:
        form = AppConfigForm()

    return render(
        request,
        'core/config_form.html',
        {
            'page_title': 'Add Configuration',
            'form': form,
            'submit_label': 'Create Configuration',
        },
    )


@login_required
def config_update(request, pk):
    config = get_object_or_404(AppConfig, pk=pk)
    if request.method == 'POST':
        form = AppConfigForm(request.POST, instance=config)
        if form.is_valid():
            config = form.save(commit=False)
            config.updated_by = request.user
            config.save()
            messages.success(request, 'Configuration updated successfully.')
            return redirect('core:config_detail', pk=config.pk)
    else:
        form = AppConfigForm(instance=config)

    return render(
        request,
        'core/config_form.html',
        {
            'page_title': 'Edit Configuration',
            'form': form,
            'config': config,
            'submit_label': 'Save Changes',
        },
    )


@login_required
def config_deactivate(request, pk):
    config = get_object_or_404(AppConfig, pk=pk)
    if request.method == 'POST':
        config.is_active = False
        config.updated_by = request.user
        config.save(update_fields=['is_active', 'updated_by', 'updated_at'])
        messages.success(request, 'Configuration deactivated successfully.')
        return redirect('core:config_list')

    return render(
        request,
        'core/config_confirm_deactivate.html',
        {
            'page_title': 'Deactivate Configuration',
            'config': config,
        },
    )
