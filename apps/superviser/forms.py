# coding=utf-8
from django import forms
from apps.superviser.models import Superviser
from core.models import User

__author__ = 'alexy'


class SuperviserAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'patronymic', 'phone')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    password1 = forms.CharField(label=u'Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        data = self.cleaned_data
        try:
            User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return data['email']
        raise forms.ValidationError(u'Пользователь с таким e-mail уже зарегистрирован')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'Пароль и подтверждение пароля не совпадают!')
        return password2

    def save(self, commit=True):
        user = super(SuperviserAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SuperviserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'patronymic', 'phone')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SuperviserCityForm(forms.ModelForm):
    class Meta:
        model = Superviser
        fields = '__all__'
        widgets = {
            'superviser': forms.HiddenInput(),
            'city': forms.CheckboxSelectMultiple(),
        }
