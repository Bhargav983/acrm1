from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import APIDataForm, ASTROLOGY_PLANETS, HOUSE_NUMBERS, CustomerForm
from .models import APIData, Customer


def build_api_manual_entry_rows(api_data):
    entries = {}
    if isinstance(api_data.parsed_response, dict):
        entries = api_data.parsed_response.get('manual_entries', {})

    planet_sign_rows = []
    planet_house_rows = []
    planet_nakshatra_rows = []
    for slug, label in ASTROLOGY_PLANETS:
        planet_sign_rows.append(
            {
                'planet': label,
                'sign': entries.get(f'planet_sign_{slug}', ''),
                'lord': entries.get(f'planet_sign_{slug}_lord', ''),
                'relationship': entries.get(f'planet_sign_{slug}_relationship', ''),
            }
        )
        planet_house_rows.append(
            {
                'planet': label,
                'house': entries.get(f'planet_house_{slug}', ''),
            }
        )
        planet_nakshatra_rows.append(
            {
                'planet': label,
                'nakshatra': entries.get(f'planet_nakshatra_{slug}', ''),
                'pada': entries.get(f'planet_nakshatra_{slug}_pada', ''),
                'owner': entries.get(f'planet_nakshatra_{slug}_owner', ''),
                'relationship': entries.get(f'planet_nakshatra_{slug}_relationship', ''),
            }
        )

    house_lord_rows = []
    for house_number, house_label in HOUSE_NUMBERS:
        house_lord_rows.append(
            {
                'house': house_label,
                'source_sign': entries.get(f'house_lord_{house_number}_source_sign', ''),
                'lord_planet': entries.get(f'house_lord_{house_number}_lord_planet', ''),
                'destination_house': entries.get(f'house_lord_{house_number}_destination_house', ''),
                'destination_sign': entries.get(f'house_lord_{house_number}_destination_sign', ''),
                'relationship': entries.get(f'house_lord_{house_number}_relationship', ''),
            }
        )

    return {
        'planet_sign_rows': planet_sign_rows,
        'planet_house_rows': planet_house_rows,
        'planet_nakshatra_rows': planet_nakshatra_rows,
        'house_lord_rows': house_lord_rows,
        'has_planet_sign_rows': any(
            row['sign'] or row['lord'] or row['relationship'] for row in planet_sign_rows
        ),
        'has_planet_house_rows': any(row['house'] for row in planet_house_rows),
        'has_planet_nakshatra_rows': any(
            row['nakshatra'] or row['pada'] or row['owner'] or row['relationship']
            for row in planet_nakshatra_rows
        ),
        'has_house_lord_rows': any(
            row['source_sign']
            or row['lord_planet']
            or row['destination_house']
            or row['destination_sign']
            or row['relationship']
            for row in house_lord_rows
        ),
    }


@login_required
def customer_list(request):
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'active')
    customers = Customer.objects.all()

    if status_filter == 'active':
        customers = customers.filter(is_active=True)
    elif status_filter == 'inactive':
        customers = customers.filter(is_active=False)

    if search_query:
        search_filter = (
            Q(customer_name__icontains=search_query)
            | Q(mobile_number__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(place_of_birth__icontains=search_query)
            | Q(occupation__icontains=search_query)
            | Q(education__icontains=search_query)
            | Q(api_data_records__nakshatra__icontains=search_query)
        )
        if search_query.isdigit():
            search_filter |= Q(api_data_records__pada=int(search_query))
        customers = customers.filter(search_filter).distinct()

    return render(
        request,
        'customers/customer_list.html',
        {
            'page_title': 'Customers',
            'customers': customers,
            'search_query': search_query,
            'status_filter': status_filter,
        },
    )


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    latest_api_data = customer.api_data_records.filter(is_active=True).first()
    return render(
        request,
        'customers/customer_detail.html',
        {
            'page_title': customer.customer_name,
            'customer': customer,
            'latest_api_data': latest_api_data,
        },
    )


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.updated_by = request.user
            customer.save()
            messages.success(request, 'Customer created successfully.')
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()

    return render(
        request,
        'customers/customer_form.html',
        {
            'page_title': 'Add Customer',
            'form': form,
            'submit_label': 'Create Customer',
        },
    )


@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_by = request.user
            customer.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)

    return render(
        request,
        'customers/customer_form.html',
        {
            'page_title': 'Edit Customer',
            'form': form,
            'customer': customer,
            'submit_label': 'Save Changes',
        },
    )


@login_required
def customer_deactivate(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.is_active = False
        customer.updated_by = request.user
        customer.save(update_fields=['is_active', 'updated_by', 'updated_at'])
        messages.success(request, 'Customer deactivated successfully.')
        return redirect('customers:customer_list')

    return render(
        request,
        'customers/customer_confirm_deactivate.html',
        {
            'page_title': 'Deactivate Customer',
            'customer': customer,
        },
    )


@login_required
def api_data_list(request):
    search_query = request.GET.get('q', '').strip()
    source_filter = request.GET.get('source', '')
    status_filter = request.GET.get('status', 'active')
    api_records = APIData.objects.select_related('customer').all()

    if status_filter == 'active':
        api_records = api_records.filter(is_active=True)
    elif status_filter == 'inactive':
        api_records = api_records.filter(is_active=False)

    if source_filter:
        api_records = api_records.filter(data_source=source_filter)

    if search_query:
        search_filter = (
            Q(customer__customer_name__icontains=search_query)
            | Q(customer__mobile_number__icontains=search_query)
            | Q(api_provider__icontains=search_query)
            | Q(api_name__icontains=search_query)
            | Q(lagna__icontains=search_query)
            | Q(moon_sign__icontains=search_query)
            | Q(sun_sign__icontains=search_query)
            | Q(nakshatra__icontains=search_query)
            | Q(current_mahadasha__icontains=search_query)
            | Q(current_antardasha__icontains=search_query)
        )
        if search_query.isdigit():
            search_filter |= Q(pada=int(search_query))
        api_records = api_records.filter(search_filter)

    return render(
        request,
        'customers/api_data_list.html',
        {
            'page_title': 'Astrology Data',
            'api_records': api_records,
            'search_query': search_query,
            'source_filter': source_filter,
            'status_filter': status_filter,
            'data_source_choices': APIData.DATA_SOURCE_CHOICES,
        },
    )


@login_required
def api_data_detail(request, pk):
    api_data = get_object_or_404(APIData.objects.select_related('customer'), pk=pk)
    manual_entry_rows = build_api_manual_entry_rows(api_data)
    return render(
        request,
        'customers/api_data_detail.html',
        {
            'page_title': 'Astrology Data',
            'api_data': api_data,
            **manual_entry_rows,
        },
    )


@login_required
def api_data_create(request):
    if request.method == 'POST':
        form = APIDataForm(request.POST)
        if form.is_valid():
            api_data = form.save()
            messages.success(request, 'Astrology data record created successfully.')
            return redirect('customers:api_data_detail', pk=api_data.pk)
    else:
        initial = {}
        customer_id = request.GET.get('customer')
        if customer_id:
            initial['customer'] = customer_id
        form = APIDataForm(initial=initial)

    return render(
        request,
        'customers/api_data_form.html',
        {
            'page_title': 'Add Astrology Data',
            'form': form,
            'submit_label': 'Create Record',
        },
    )


@login_required
def api_data_update(request, pk):
    api_data = get_object_or_404(APIData, pk=pk)
    if request.method == 'POST':
        form = APIDataForm(request.POST, instance=api_data)
        if form.is_valid():
            api_data = form.save()
            messages.success(request, 'Astrology data record updated successfully.')
            return redirect('customers:api_data_detail', pk=api_data.pk)
    else:
        form = APIDataForm(instance=api_data)

    return render(
        request,
        'customers/api_data_form.html',
        {
            'page_title': 'Edit Astrology Data',
            'form': form,
            'api_data': api_data,
            'submit_label': 'Save Changes',
        },
    )


@login_required
def api_data_deactivate(request, pk):
    api_data = get_object_or_404(APIData, pk=pk)
    if request.method == 'POST':
        api_data.is_active = False
        api_data.save(update_fields=['is_active', 'updated_at'])
        messages.success(request, 'Astrology data record deactivated successfully.')
        return redirect('customers:api_data_list')

    return render(
        request,
        'customers/api_data_confirm_deactivate.html',
        {
            'page_title': 'Deactivate Astrology Data',
            'api_data': api_data,
        },
    )
