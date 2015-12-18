# coding=utf-8
from django import forms
from apps.city.models import City
from apps.client.models import Client, ClientSurface
from core.models import User

__author__ = 'alexy'


class ClientUserAddForm(forms.ModelForm):
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
        user = super(ClientUserAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.type = 3
        if commit:
            user.save()
        return user


class ClientUserUpdateForm(forms.ModelForm):
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


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = []
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control hide'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'bik': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.TextInput(attrs={'class': 'form-control'}),
            'account_cor': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_post_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_name_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_doc_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ClientUpdateForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)


class ClientAddForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['user', ]
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'bik': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.TextInput(attrs={'class': 'form-control'}),
            'account_cor': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_post_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_name_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_doc_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ClientAddForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)


class ClientSurfaceAddForm(forms.ModelForm):
    class Meta:
        model = ClientSurface
        fields = ('client', 'surface', 'date')
        widgets = {
            'client': forms.HiddenInput(attrs={'class': 'form-control'}),
            'surface': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
        }
