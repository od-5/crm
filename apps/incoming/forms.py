# coding=utf-8
from django import forms
from core.models import User
from .models import IncomingClient, IncomingTask

__author__ = 'alexy'


class IncomingClientForm(forms.ModelForm):
    class Meta:
        model = IncomingClient
        fields = '__all__'
        widgets = {
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kind_of_activity': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'fax': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'site': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
        }


class IncomingTaskForm(forms.ModelForm):
    class Meta:
        model = IncomingTask
        fields = '__all__'
        widgets = {
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'incomingclient': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': u'Текст комментария к задаче'}),
        }

