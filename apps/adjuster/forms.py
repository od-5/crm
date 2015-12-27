# coding=utf-8
from django import forms
from apps.adjuster.models import Adjuster, AdjusterTask
from apps.city.models import City, Surface
from apps.client.models import Client
from core.models import User

__author__ = 'alexy'


class AdjusterUserAddForm(forms.ModelForm):
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
        user = super(AdjusterUserAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.type = 4
        if commit:
            user.save()
        return user


class AdjusterAddForm(forms.ModelForm):
    class Meta:
        model = Adjuster
        exclude = ['user', ]
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdjusterAddForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)


class AdjusterUpdateForm(forms.ModelForm):
    class Meta:
        model = Adjuster
        exclude = []
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control hide'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdjusterUpdateForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)


class AdjusterUserUpdateForm(forms.ModelForm):
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


class AdjusterTaskAddForm(forms.ModelForm):
    class Meta:
        model = AdjusterTask
        fields = ('adjuster', 'type', 'date', 'comment')
        widgets = {
            'adjuster': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

    client = forms.ModelChoiceField(queryset=Client.objects.all(), label=u'Клиент', widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdjusterTaskAddForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['adjuster'].queryset = Adjuster.objects.filter(city__moderator=self.request.user)
            self.fields['client'].queryset = Client.objects.filter(city__moderator=self.request.user)
