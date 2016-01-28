# coding=utf-8
from django.forms import ModelForm, TextInput, Select, DateInput, HiddenInput
from core.models import User
from .models import City, Street, Area, ManagementCompany

__author__ = 'alexy'


class CityAddForm(ModelForm):
    class Meta:
        model = City
        fields = ('name', 'moderator', 'contract_number', 'contract_date')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'moderator': Select(attrs={'class': 'form-control'}),
            'contract_number': TextInput(attrs={'class': 'form-control'}),
            'contract_date': DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CityAddForm, self).__init__(*args, **kwargs)
        self.fields['moderator'].queryset = User.objects.filter(type=2)


class AreaAddForm(ModelForm):
    class Meta:
        model = Area
        fields = ('city', 'name', )
        widgets = {
            'city': HiddenInput(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
        }


class StreetForm(ModelForm):
    class Meta:
        model = Street
        fields = ('city', 'area', 'name')
        widgets = {
            'city': HiddenInput(attrs={'class': 'form-control'}),
            'area': Select(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
        }


class ManagementCompanyForm(ModelForm):
    class Meta:
        model = ManagementCompany
        fields = '__all__'
        widgets = {
            'city': Select(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'leader_function': TextInput(attrs={'class': 'form-control'}),
            'leader_name': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ManagementCompanyForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)
