from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Player

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['full_name', 'birth_date', 'profile_photo']
