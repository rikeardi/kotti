from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *


class KottiUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = KottiUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'department', 'team')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class KottiUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = KottiUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'department', 'team', 'password', 'is_active', 'is_admin')


class KottiUserAdmin(UserAdmin):
    form = KottiUserChangeForm
    add_form = KottiUserCreationForm

    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'department', 'team')
    fieldsets = ((None, {'fields': ('username', 'email', 'password')}),
                 ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
                 ('Team info', {'fields': ('department', 'team')}),
                 ('Permissions', {'fields': ('is_active', 'is_admin')}))

    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('username', 'email', 'first_name', 'last_name', 'phone', 'department', 'team', 'password1', 'password2')}),)


admin.site.register(KottiUser, KottiUserAdmin)
admin.site.unregister(Group)
admin.site.register(OpenTime)
admin.site.register(Room)
admin.site.register(Table)
admin.site.register(TableReservation)
