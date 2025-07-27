from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Program, SubProgram, Child, Enrollment, User
from .forms import ProgramForm, SubProgramForm, ChildForm, EnrollmentForm
from django.contrib import messages
from django.db.models import Q

def home_view(request):
    programs = Program.objects.all()
    return render(request, 'academy/home.html', {'programs': programs})


def subprogram_list_view(request, sport_slug):
    parent_program = get_object_or_404(Program, sport_type__iexact=sport_slug)
    subprograms = SubProgram.objects.filter(program=parent_program)

    return render(request, 'academy/subprogram_list.html', {
        'parent_program': parent_program,
        'subprograms': subprograms,
        'show_create_subprogram': request.user.is_authenticated and request.user.role in ['admin', 'coach'],
        'sport_slug': sport_slug,
    })



def is_admin_or_coach(user):
    return user.is_authenticated and user.role in ['admin', 'coach']

@user_passes_test(is_admin_or_coach)
def program_create_view(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Program created successfully!")
            return redirect('academy:home')
    else:
        form = ProgramForm()
    return render(request, 'academy/program_form.html', {'form': form})


@user_passes_test(is_admin_or_coach)
def subprogram_create_view(request, sport_slug):
    parent_program = get_object_or_404(Program, sport_type__iexact=sport_slug)

    if request.method == 'POST':
        form = SubProgramForm(request.POST or None, request.FILES or None, user=request.user)
        if form.is_valid():
            subprogram = form.save(commit=False)
            subprogram.program = parent_program

            if request.user.role == 'coach':
                subprogram.coach = request.user
            else:
                coach = User.objects.filter(role='coach', sport=parent_program.sport_type).first()
                subprogram.coach = coach

            subprogram.save()
            messages.success(request, "SubProgram created successfully!")
            return redirect('academy:subprogram_list', sport_slug=sport_slug)
    else:
        form = SubProgramForm()

    return render(request, 'academy/subprogram_form.html', {
        'form': form,
        'parent_program': parent_program
    })



@login_required
def child_create_view(request):
    if request.user.role != 'parent':
        return redirect('academy:home')

    if request.method == 'POST':
        form = ChildForm(request.POST, request.FILES)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            messages.success(request, "Child added successfully!")
            return redirect('academy:home')
    else:
        form = ChildForm()
    return render(request, 'academy/child_form.html', {'form': form})


@login_required
def child_list_view(request):
    if request.user.role != 'parent':
        return redirect('academy:home')

    children = Child.objects.filter(parent=request.user)
    return render(request, 'academy/child_list.html', {'children': children})


@login_required
def enroll_child_view(request, subprogram_id):
    subprogram = get_object_or_404(SubProgram, id=subprogram_id)

    if request.user.role != 'parent':
        return redirect('academy:home')

    form = EnrollmentForm()
    form.fields['child'].queryset = Child.objects.filter(parent=request.user)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        form.fields['child'].queryset = Child.objects.filter(parent=request.user)

        if form.is_valid():
            child = form.cleaned_data['child']

            same_sport_enrolled = Enrollment.objects.filter(
                child=child,
                subprogram__program__sport_type=subprogram.program.sport_type
            ).exists()

            already_enrolled = Enrollment.objects.filter(
                child=child, subprogram=subprogram
            ).exists()

            if already_enrolled:
                messages.error(request, f"{child.name} is already enrolled in this program.")
                return redirect('academy:subprogram_list', sport_slug=subprogram.program.sport_type)

            if same_sport_enrolled:
                messages.error(request, f"{child.name} is already enrolled in another {subprogram.program.get_sport_type_display()} program.")
                return redirect('academy:subprogram_list', sport_slug=subprogram.program.sport_type)

            enrollment = form.save(commit=False)
            enrollment.subprogram = subprogram
            enrollment.save()
            messages.success(request, f"{child.name} enrolled successfully in {subprogram.title}!")
            return redirect('academy:child_list')

    return render(request, 'academy/enroll_form.html', {
        'form': form,
        'subprogram': subprogram
    })


@login_required
def child_update_view(request, child_id):
    child = get_object_or_404(Child, id=child_id, parent=request.user)
    
    if request.method == 'POST':
        form = ChildForm(request.POST, request.FILES, instance=child)
        if form.is_valid():
            form.save()
            messages.success(request, "Child updated successfully!")
            return redirect('academy:child_list')
    else:
        form = ChildForm(instance=child)

    return render(request, 'academy/child_form.html', {'form': form})

@login_required
def child_delete_view(request, child_id):
    child = get_object_or_404(Child, id=child_id, parent=request.user)

    if request.method == 'POST':
        child.delete()
        messages.success(request, "Child deleted successfully!")
        return redirect('academy:child_list')

    return render(request, 'academy/child_confirm_delete.html', {'child': child})

@user_passes_test(is_admin_or_coach)
def subprogram_update_view(request, subprogram_id):
    subprogram = get_object_or_404(SubProgram, id=subprogram_id)

    if request.method == 'POST':
        form = SubProgramForm(request.POST or None, request.FILES or None, instance=subprogram, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "SubProgram updated successfully!")
            return redirect('academy:subprogram_list', sport_slug=subprogram.program.sport_type)
    else:
        form = SubProgramForm(instance=subprogram)

    return render(request, 'academy/subprogram_form.html', {
        'form': form,
        'parent_program': subprogram.program,
    })

@user_passes_test(is_admin_or_coach)
def subprogram_delete_view(request, subprogram_id):
    subprogram = get_object_or_404(SubProgram, id=subprogram_id)

    if request.method == 'POST':
        subprogram.delete()
        messages.success(request, "SubProgram deleted successfully!")
        return redirect('academy:subprogram_list', sport_slug=subprogram.program.sport_type)

    return render(request, 'academy/subprogram_confirm_delete.html', {'subprogram': subprogram})

@user_passes_test(is_admin_or_coach)
def program_update_view(request, program_id):
    program = get_object_or_404(Program, id=program_id)

    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, "Program updated successfully!")
            return redirect('academy:home')  
    else:
        form = ProgramForm(instance=program)

    return render(request, 'academy/program_form.html', {'form': form, 'update': True})

@user_passes_test(is_admin_or_coach)
def program_delete_view(request, program_id):
    program = get_object_or_404(Program, id=program_id)

    if request.method == 'POST':
        program.delete()
        messages.success(request, "Program deleted successfully!")
        return redirect('academy:home')

    return render(request, 'academy/program_confirm_delete.html', {'program': program})

@login_required
def child_update_view(request, child_id):
    child = get_object_or_404(Child, id=child_id, parent=request.user)

    if request.method == 'POST':
        form = ChildForm(request.POST, request.FILES, instance=child)
        if form.is_valid():
            form.save()
            messages.success(request, "Child information updated successfully!")
            return redirect('academy:child_list')
    else:
        form = ChildForm(instance=child)

    return render(request, 'academy/child_form.html', {'form': form})

@login_required
def child_delete_view(request, child_id):
    child = get_object_or_404(Child, id=child_id, parent=request.user)

    if request.method == 'POST':
        child.delete()
        messages.success(request, "Child deleted successfully!")
        return redirect('academy:child_list')

    return render(request, 'academy/child_confirm_delete.html', {'child': child})

def is_coach(user):
    return user.is_authenticated and user.role == 'coach'

@login_required
@user_passes_test(is_coach)
def coach_dashboard_view(request):
    coach = request.user
    query = request.GET.get('q', '')
    age_range = request.GET.get('age', '')

    subprograms = SubProgram.objects.filter(coach=coach).order_by('-start_date')
    subprograms_with_children = []

    #to search the age (dictionary)
    age_filters = {
        '6-8': (6, 8),
        '8-10': (8, 10),
        '10-12': (10, 12),
        '12-14': (12, 14),
        '14-16': (14, 16),
    }

    for sp in subprograms:
        enrolled_qs = Enrollment.objects.filter(subprogram=sp).select_related('child', 'child__parent')

        if query:
            enrolled_qs = enrolled_qs.filter(child__name__icontains=query)

        if age_range in age_filters:
            min_age, max_age = age_filters[age_range]
            enrolled_qs = enrolled_qs.filter(child__age__gte=min_age, child__age__lt=max_age)

        subprograms_with_children.append((sp, enrolled_qs))

    context = {
        'subprograms_with_children': subprograms_with_children,
        'query': query,
        'age_range': age_range,
        'age_options': ['6-8', '8-10', '10-12', '12-14', '14-16'],
    }
    return render(request, 'academy/coach_dashboard.html', context)



