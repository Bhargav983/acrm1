from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ConsultationNoteForm
from .models import ConsultationNote


@login_required
def consultation_list(request):
    search_query = request.GET.get('q', '').strip()
    follow_up_filter = request.GET.get('follow_up', '')
    date_filter = request.GET.get('date', '').strip()
    active_filter = request.GET.get('active', 'active')
    consultations = ConsultationNote.objects.select_related(
        'customer',
        'created_by',
        'updated_by',
    )

    if active_filter == 'active':
        consultations = consultations.filter(is_active=True)
    elif active_filter == 'inactive':
        consultations = consultations.filter(is_active=False)

    if follow_up_filter == 'yes':
        consultations = consultations.filter(follow_up_required=True)
    elif follow_up_filter == 'no':
        consultations = consultations.filter(follow_up_required=False)

    if date_filter:
        consultations = consultations.filter(consultation_date__date=date_filter)

    if search_query:
        consultations = consultations.filter(
            Q(customer__customer_name__icontains=search_query)
            | Q(topic__icontains=search_query)
            | Q(notes__icontains=search_query)
        )

    return render(
        request,
        'consultations/consultation_list.html',
        {
            'page_title': 'Consultations',
            'consultations': consultations,
            'search_query': search_query,
            'follow_up_filter': follow_up_filter,
            'date_filter': date_filter,
            'active_filter': active_filter,
        },
    )


@login_required
def consultation_detail(request, pk):
    consultation = get_object_or_404(
        ConsultationNote.objects.select_related('customer', 'created_by', 'updated_by'),
        pk=pk,
    )
    return render(
        request,
        'consultations/consultation_detail.html',
        {
            'page_title': 'Consultation Detail',
            'consultation': consultation,
        },
    )


@login_required
def consultation_create(request):
    if request.method == 'POST':
        form = ConsultationNoteForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.created_by = request.user
            consultation.updated_by = request.user
            consultation.save()
            messages.success(request, 'Consultation note created successfully.')
            return redirect('consultations:consultation_detail', pk=consultation.pk)
    else:
        initial = {}
        customer_id = request.GET.get('customer')
        if customer_id:
            initial['customer'] = customer_id
        form = ConsultationNoteForm(initial=initial)

    return render(
        request,
        'consultations/consultation_form.html',
        {
            'page_title': 'Add Consultation',
            'form': form,
            'submit_label': 'Create Consultation',
        },
    )


@login_required
def consultation_update(request, pk):
    consultation = get_object_or_404(ConsultationNote, pk=pk)
    if request.method == 'POST':
        form = ConsultationNoteForm(request.POST, instance=consultation)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.updated_by = request.user
            consultation.save()
            messages.success(request, 'Consultation note updated successfully.')
            return redirect('consultations:consultation_detail', pk=consultation.pk)
    else:
        form = ConsultationNoteForm(instance=consultation)

    return render(
        request,
        'consultations/consultation_form.html',
        {
            'page_title': 'Edit Consultation',
            'form': form,
            'consultation': consultation,
            'submit_label': 'Save Changes',
        },
    )


@login_required
def consultation_deactivate(request, pk):
    consultation = get_object_or_404(ConsultationNote, pk=pk)
    if request.method == 'POST':
        consultation.is_active = False
        consultation.updated_by = request.user
        consultation.save(update_fields=['is_active', 'updated_by', 'updated_at'])
        messages.success(request, 'Consultation note deactivated successfully.')
        return redirect('consultations:consultation_list')

    return render(
        request,
        'consultations/consultation_confirm_deactivate.html',
        {
            'page_title': 'Deactivate Consultation',
            'consultation': consultation,
        },
    )
