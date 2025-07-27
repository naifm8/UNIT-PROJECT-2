from django import forms
from .models import Program, SubProgram, Child, Enrollment, User

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['sport_type', 'image']


class SubProgramForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    class Meta:
        model = SubProgram
        fields = ['title', 'gender', 'min_age', 'max_age', 'start_date', 'description', 'duration_weeks', 'image', 'coach']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['coach'].queryset = User.objects.filter(role='coach')

        if user and user.role != 'admin':
            self.fields.pop('coach')


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'age', 'gender', 'image']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['child']

