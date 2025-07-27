from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

#this is for the coach creat 
SPORT_CHOICES = [
    ('football', 'Football'),
    ('basketball', 'Basketball'),
    ('tennis', 'Tennis'),
]

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

SPORT_CHOICES = [
    ('Football', 'Football'),
    ('Basketball', 'Basketball'),
    ('Tennis', 'Tennis'),
]

class RegisterUserForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('parent', 'Parent'), ('coach', 'Coach')], widget=forms.Select(attrs={'id': 'id_role'}))
    sport = forms.ChoiceField(choices=SPORT_CHOICES, required=False, widget=forms.Select(attrs={'id': 'id_sport'}))
    experience_years = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'id': 'id_experience_years'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'sport', 'experience_years', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('role') == 'coach':
            if not cleaned_data.get('sport') or not cleaned_data.get('experience_years'):
                raise forms.ValidationError("Sport and Experience are required for coaches.")
        return cleaned_data


class CustomUserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class AdminAddUserForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('parent', 'Parent'), ('coach', 'Coach')])
    sport = forms.ChoiceField(choices=SPORT_CHOICES, required=False)
    experience_years = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'sport', 'experience_years', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('role') == 'coach':
            if not cleaned_data.get('sport') or not cleaned_data.get('experience_years'):
                raise forms.ValidationError("Sport and Experience are required for coaches.")
        return cleaned_data


