from django.shortcuts import render, redirect, get_object_or_404
from .models import Program, Enrollment
from accounts.models import Player
from .forms import EnrollmentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test #!!!!!!!!!
from .forms import ProgramForm, SubProgramForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def program_list_view(request):
    sport_filter = request.GET.get('sport')
    age_filter = request.GET.get('age')

    programs = Program.objects.all()

    if sport_filter:
        programs = programs.filter(sport=sport_filter)

    if age_filter and age_filter.isdigit():
        age = int(age_filter)
        programs = programs.filter(min_age__lte=age, max_age__gte=age)

    context = {
        'programs': programs,
        'selected_sport': sport_filter,
        'selected_age': age_filter,
        'sports': Program.SPORT_CHOICES,
        'age_options': [6, 8, 10, 12, 14, 16],
    }
    return render(request, 'academy/program_list.html', context)


@login_required
def enroll_player_view(request, program_id):
    if request.user.role != 'parent':
        return HttpResponseForbidden("Only parents can enroll players.")

    program = get_object_or_404(Program, id=program_id)
    players = Player.objects.filter(parent=request.user)

    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = get_object_or_404(Player, id=player_id, parent=request.user)

        player_age = player.age
        if not (program.min_age <= player_age <= program.max_age):
            return render(request, 'academy/enrollment_result.html', {
                'message': f"{player.full_name} is not eligible for this program. Age must be between {program.min_age} and {program.max_age}."
                })

        if Enrollment.objects.filter(player=player, program=program).exists():
            return render(request, 'academy/enrollment_result.html', {
                'message': 'Player already enrolled in this program.'
                })

        Enrollment.objects.create(player=player, program=program)
        return render(request, 'academy/enrollment_result.html', {
            'message': f'{player.full_name} has been enrolled in {program.title}.'
            })

    return render(request, 'academy/enroll_player.html', {
        'program': program,
        'players': players
    })


User = get_user_model()
@user_passes_test(lambda u: u.is_authenticated and u.role in ['coach', 'admin'])
def program_create_view(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            program = form.save(commit=False)
            # Admin can assign coach, Coach assigns self
            if request.user.role == 'coach':
                program.coach = request.user
            program.save()
            return redirect('academy:program_list')
    else:
        form = ProgramForm()

        # Hide coach field for coach role
        if request.user.role == 'coach' and 'coach' in form.fields:
            form.fields.pop('coach')

    return render(request, 'academy/program_form.html', {'form': form})


@login_required
def program_detail_view(request, pk):
    program = get_object_or_404(Program, pk=pk)

    # Count all enrollments (or only approved if preferred)
    total_players = program.enrollment_set.filter(status='approved').count()

    return render(request, 'academy/program_detail.html', {
        'program': program,
        'total_players': total_players,
    })


@login_required
def program_list_view(request):
    sport_filter = request.GET.get('sport')
    age_filter = request.GET.get('age')
    query = request.GET.get('q')

    programs = Program.objects.all()

    if sport_filter:
        programs = programs.filter(sport=sport_filter)

    if age_filter and age_filter.isdigit():
        age = int(age_filter)
        programs = programs.filter(min_age__lte=age, max_age__gte=age)

    if query:
        programs = programs.filter(Q(title__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(programs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'programs': page_obj,
        'page_obj': page_obj,
        'selected_sport': sport_filter,
        'selected_age': age_filter,
        'sports': Program.SPORT_CHOICES,
        'age_options': [6, 8, 10, 12, 14, 16],
        'query': query,
    }
    return render(request, 'academy/program_list.html', context)

def subprogram_list_view(request, program_id):
    main_program = get_object_or_404(Program, id=program_id)
    subprograms = main_program.subprograms.all()  # from related_name
    return render(request, 'academy/subprogram_list.html', {
        'main_program': main_program,
        'subprograms': subprograms
    })

def is_admin_or_coach(user):
    return user.is_authenticated and user.role in ['admin', 'coach']

@login_required
@user_passes_test(is_admin_or_coach)
def subprogram_create_view(request, parent_id):
    parent_program = get_object_or_404(Program, id=parent_id)

    if request.method == 'POST':
        form = SubProgramForm(request.POST, request.FILES)
        if form.is_valid():
            subprogram = form.save(commit=False)
            subprogram.parent = parent_program
            subprogram.sport = parent_program.sport
            subprogram.coach = request.user
            subprogram.save()
            return redirect('academy:subprogram_list', program_id=parent_program.id)
    else:
        form = SubProgramForm()

    return render(request, 'academy/subprogram_form.html', {
        'form': form,
        'parent_program': parent_program
    })





@login_required
def program_edit_view(request, pk):
    program = get_object_or_404(Program, pk=pk)

    # Only the assigned coach or admin can edit
    if request.user.role == 'coach' and program.coach != request.user:
        return HttpResponseForbidden("You cannot edit this program.")

    if request.user.role == 'coach':
        form = ProgramForm(request.POST or None, instance=program)
        form.fields.pop('coach')  # coach can't change coach field
    else:
        form = ProgramForm(request.POST or None, instance=program)

    if request.method == 'POST' and form.is_valid():
        updated = form.save(commit=False)
        if request.user.role == 'coach':
            updated.coach = request.user  # reassign to self just in case
        updated.save()
        return redirect('academy:program_list')

    return render(request, 'academy/program_form.html', {'form': form, 'editing': True})

@login_required
def program_delete_view(request, pk):
    program = get_object_or_404(Program, pk=pk)

    # Only the assigned coach or admin can delete
    if request.user.role == 'coach' and program.coach != request.user:
        return HttpResponseForbidden("You cannot delete this program.")

    if request.method == 'POST':
        program.delete()
        return redirect('academy:program_list')

    return render(request, 'academy/program_confirm_delete.html', {'program': program})


def is_admin_or_coach(user):
    return user.is_authenticated and user.role in ['admin', 'coach']

@user_passes_test(is_admin_or_coach) #!!!!!!!!!!!!
def pending_enrollments_view(request):
    if request.user.role == 'admin':
        enrollments = Enrollment.objects.filter(status='pending').select_related('program', 'player')
    else:  # coach
        enrollments = Enrollment.objects.filter(
            status='pending',
            program__coach=request.user
        ).select_related('program', 'player')

    return render(request, 'academy/pending_enrollments.html', {
        'enrollments': enrollments
    })

@user_passes_test(is_admin_or_coach)
def approve_enrollment_view(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    # Access control: coach can only approve their own program enrollments
    if request.user.role == 'coach' and enrollment.program.coach != request.user:
        return HttpResponseForbidden("You can't approve this enrollment.")

    enrollment.status = 'approved'
    enrollment.save()
    return redirect('academy:pending_enrollments')

@user_passes_test(is_admin_or_coach)
def reject_enrollment_view(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if request.user.role == 'coach' and enrollment.program.coach != request.user:
        return HttpResponseForbidden("You can't reject this enrollment.")

    enrollment.status = 'rejected'
    enrollment.save()
    return redirect('academy:pending_enrollments')
