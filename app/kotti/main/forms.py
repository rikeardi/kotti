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

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'input'}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input'}))
    department = forms.CharField(widget=forms.Select(choices=[('LT', 'Leiritoimikunta'), ('EL', 'Elämys'),
                                                            ('OS', 'Osallistujat'), ('PA', 'Palvelut'),
                                                            ('KA', 'Kasvatus'), ('RE', 'Resurssit')],
                                                            attrs={'class': 'input'}))
    team = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input'}))

    class Meta(UserCreationForm.Meta):
        model = KottiUser
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'department', 'team', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.department = self.cleaned_data['department']
        user.team = self.cleaned_data['team']

        if commit:
            user.save()
        return user
