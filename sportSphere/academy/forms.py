from django import forms
from .models import Program, Enrollment

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['sport', 'image'] 

class SubProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        exclude = ['sport', 'parent'] 


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = []  # this is botton to enroll
