# coding=utf-8
from django.forms import ModelForm, TextInput, Select, DateInput
from django import forms
from .models import City

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
