from django import forms
from .models import Program, Enrollment

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['sport', 'title', 'description', 'min_age', 'max_age', 'start_date', 'duration_weeks', 'coach']


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = []  # this is botton to enroll
