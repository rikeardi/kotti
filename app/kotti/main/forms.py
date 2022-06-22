from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input'}))


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'input'}))
    phone = forms.CharField(widget=forms.TextInput())
    department = forms.ModelChoiceField(widget=forms.Select(), queryset=Department.objects.all())
    team = forms.ModelChoiceField(widget=forms.Select(), queryset=Team.objects.all())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

