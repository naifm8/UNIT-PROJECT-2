from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import UserRegistrationForm, PlayerForm
from .models import Player, User
from academy.models import Enrollment
from academy.models import Program, Enrollment

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'parent':
                return redirect('accounts:player_add')
            return redirect('academy:program_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accounts:dashboard')

        else:
            error = "Invalid credentials"
            return render(request, 'accounts/login.html', {'error': error})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def player_list_view(request):
    # Parents see only their own players; admins see all; coaches read-only (here: all)
    if request.user.role == 'parent':
        players = Player.objects.filter(parent=request.user)
    else:
        players = Player.objects.all()

    players = players.prefetch_related('enrollment_set__program')    
    return render(request, 'accounts/player_list.html', {'players': players})

@login_required
def player_add_view(request):
    if request.user.role != 'parent':
        return HttpResponseForbidden("Only parents can add players.")
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            player = form.save(commit=False)
            player.parent = request.user
            player.save()
            # After adding, go to player list OR directly enroll flow later
            return redirect('accounts:player_list')
    else:
        form = PlayerForm()
    return render(request, 'accounts/player_form.html', {'form': form, 'action': 'Add'})

@login_required
def player_update_view(request, pk):
    player = get_object_or_404(Player, pk=pk)
    # Parents can edit only their own player; admins can edit any
    if request.user.role == 'parent' and player.parent != request.user:
        return HttpResponseForbidden("Not allowed.")
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return redirect('accounts:player_list')
    else:
        form = PlayerForm(instance=player)
    return render(request, 'accounts/player_form.html', {'form': form, 'action': 'Edit'})

@login_required
def player_delete_view(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if request.user.role == 'parent' and player.parent != request.user:
        return HttpResponseForbidden("Not allowed.")
    if request.method == 'POST':
        player.delete()
        return redirect('accounts:player_list')
    return render(request, 'accounts/player_confirm_delete.html', {'player': player})

@login_required
def player_detail_view(request, pk):
    player = get_object_or_404(Player, pk=pk)

    # Access control: parent can only view their own child
    if request.user.role == 'parent' and player.parent != request.user:
        return HttpResponseForbidden("You are not allowed to view this player.")

    # Load enrollments with related program info
    enrollments = player.enrollment_set.select_related('program').order_by('-enrolled_on')

    context = {
        'player': player,
        'enrollments': enrollments,
    }
    return render(request, 'accounts/player_detail.html', context)




@login_required
def dashboard_view(request):
    user = request.user
    context = {}

    if user.role == 'parent':
        players = Player.objects.filter(parent=user)
        enrollments = Enrollment.objects.filter(player__in=players).select_related('program', 'player')
        context.update({
            'players': players,
            'enrollments': enrollments,
            'role': 'parent'
        })

    elif user.role == 'coach':
        programs = Program.objects.filter(coach=user)
        enrollments = Enrollment.objects.filter(program__in=programs).select_related('program', 'player')
        context.update({
            'programs': programs,
            'enrollments': enrollments,
            'role': 'coach'
        })

    elif user.role == 'admin':
        users = User.objects.all()
        enrollments = Enrollment.objects.all().select_related('program', 'player')
        context.update({
            'users': users,
            'enrollments': enrollments,
            'role': 'admin'
        })

    return render(request, 'accounts/dashboard.html', context)


