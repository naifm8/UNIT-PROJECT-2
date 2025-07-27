from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserLoginForm, AdminAddUserForm, RegisterUserForm
from django.contrib.auth.decorators import user_passes_test

def register_view(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('accounts:login')
    else:
        form = RegisterUserForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('academy:home')

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as DjangoUser  # fallback if needed

def login_view(request):
    if request.user.is_authenticated:
        return redirect('academy:home')

    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username_input = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Find user case-insensitively
            try:
                user_obj = User.objects.get(username__iexact=username_input)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

            if user:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('academy:home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomUserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})



def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@user_passes_test(is_admin)
def user_list_view(request):
    coaches = User.objects.filter(role='coach')
    parents = User.objects.filter(role='parent')
    return render(request, 'accounts/user_list.html', {
        'coaches': coaches,
        'parents': parents
    })

@user_passes_test(is_admin)
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_confirm_delete.html', {'user': user})

@user_passes_test(is_admin)
def add_user_view(request):
    if request.method == 'POST':
        form = AdminAddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('accounts:user_list')
    else:
        form = AdminAddUserForm()

    return render(request, 'accounts/add_user.html', {'form': form})

