from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RoleForm, UserCreateForm, UserUpdateForm
from .models import Role, User


def can_access_administration(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return bool(user.role and user.role.role_name.lower() == 'admin')


def administration_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not can_access_administration(request.user):
            messages.error(request, 'You do not have permission to access administration pages.')
            return redirect('core:dashboard')
        return view_func(request, *args, **kwargs)

    return wrapper


@administration_required
def administration(request):
    return render(request, 'accounts/administration.html', {'page_title': 'Administration'})


@administration_required
def role_list(request):
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'active')
    roles = Role.objects.all()

    if status_filter == 'active':
        roles = roles.filter(is_active=True)
    elif status_filter == 'inactive':
        roles = roles.filter(is_active=False)

    if search_query:
        roles = roles.filter(
            Q(role_name__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    return render(
        request,
        'accounts/role_list.html',
        {
            'page_title': 'Roles',
            'roles': roles,
            'search_query': search_query,
            'status_filter': status_filter,
        },
    )


@administration_required
def role_detail(request, pk):
    role = get_object_or_404(Role, pk=pk)
    return render(
        request,
        'accounts/role_detail.html',
        {
            'page_title': role.role_name,
            'role': role,
        },
    )


@administration_required
def role_create(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            messages.success(request, 'Role created successfully.')
            return redirect('accounts:role_detail', pk=role.pk)
    else:
        form = RoleForm()

    return render(
        request,
        'accounts/role_form.html',
        {
            'page_title': 'Add Role',
            'form': form,
            'submit_label': 'Create Role',
        },
    )


@administration_required
def role_update(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            messages.success(request, 'Role updated successfully.')
            return redirect('accounts:role_detail', pk=role.pk)
    else:
        form = RoleForm(instance=role)

    return render(
        request,
        'accounts/role_form.html',
        {
            'page_title': 'Edit Role',
            'form': form,
            'role': role,
            'submit_label': 'Save Changes',
        },
    )


@administration_required
def role_deactivate(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.is_active = False
        role.save(update_fields=['is_active', 'updated_at'])
        messages.success(request, 'Role deactivated successfully.')
        return redirect('accounts:role_list')

    return render(
        request,
        'accounts/role_confirm_deactivate.html',
        {
            'page_title': 'Deactivate Role',
            'role': role,
        },
    )


@administration_required
def user_list(request):
    search_query = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', 'active')
    users = User.objects.select_related('role')

    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)

    if role_filter:
        users = users.filter(role_id=role_filter)

    if search_query:
        users = users.filter(
            Q(full_name__icontains=search_query)
            | Q(username__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(mobile_number__icontains=search_query)
        )

    return render(
        request,
        'accounts/user_list.html',
        {
            'page_title': 'Users',
            'users': users,
            'roles': Role.objects.filter(is_active=True),
            'search_query': search_query,
            'role_filter': role_filter,
            'status_filter': status_filter,
        },
    )


@administration_required
def user_detail(request, pk):
    managed_user = get_object_or_404(User.objects.select_related('role'), pk=pk)
    return render(
        request,
        'accounts/user_detail.html',
        {
            'page_title': managed_user.full_name or managed_user.username,
            'managed_user': managed_user,
        },
    )


@administration_required
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            managed_user = form.save()
            messages.success(request, 'User created successfully.')
            return redirect('accounts:user_detail', pk=managed_user.pk)
    else:
        form = UserCreateForm()

    return render(
        request,
        'accounts/user_form.html',
        {
            'page_title': 'Add User',
            'form': form,
            'submit_label': 'Create User',
            'is_edit': False,
        },
    )


@administration_required
def user_update(request, pk):
    managed_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=managed_user)
        if form.is_valid():
            managed_user = form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('accounts:user_detail', pk=managed_user.pk)
    else:
        form = UserUpdateForm(instance=managed_user)

    return render(
        request,
        'accounts/user_form.html',
        {
            'page_title': 'Edit User',
            'form': form,
            'managed_user': managed_user,
            'submit_label': 'Save Changes',
            'is_edit': True,
        },
    )


@administration_required
def user_deactivate(request, pk):
    managed_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if managed_user == request.user:
            messages.error(request, 'You cannot deactivate your own account.')
            return redirect('accounts:user_detail', pk=managed_user.pk)
        managed_user.is_active = False
        managed_user.save(update_fields=['is_active', 'updated_at'])
        messages.success(request, 'User deactivated successfully.')
        return redirect('accounts:user_list')

    return render(
        request,
        'accounts/user_confirm_deactivate.html',
        {
            'page_title': 'Deactivate User',
            'managed_user': managed_user,
        },
    )
