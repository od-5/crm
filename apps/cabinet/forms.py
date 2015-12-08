# coding=utf-8
from django.forms import ModelForm, TextInput, EmailInput, Select, CharField, PasswordInput
from django import forms
from core.models import User

__author__ = 'alexy'


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'phone')
        widgets = {
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'patronymic': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
        }


class UserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'type', 'last_name', 'first_name', 'patronymic', 'phone')
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'patronymic': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
        }


class UserAddForm(ModelForm):
    password1 = CharField(label=u'Пароль', widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = CharField(label=u'Повторите пароль', widget=PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("email",)
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
