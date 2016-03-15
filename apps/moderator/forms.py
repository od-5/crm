# coding=utf-8
from django import forms
from .models import ModeratorInfo

__author__ = 'alexy'


class ModeratorInfoForm(forms.ModelForm):
    class Meta:
        model = ModeratorInfo
        fields = '__all__'
        widgets = {
            'moderator': forms.Select(attrs={'class': 'form-control'}),
            'modification': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'validity': forms.Select(attrs={'class': 'form-control'}),
            'access_restrictions': forms.Select(attrs={'class': 'form-control'}),
            'connection_contract': forms.TextInput(attrs={'class': 'form-control'}),
            'service_contract': forms.TextInput(attrs={'class': 'form-control'}),
            'contract_territory': forms.TextInput(attrs={'class': 'form-control'}),
        }
