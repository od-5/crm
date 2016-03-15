# coding=utf-8
from django import forms
from .models import Ticket

__author__ = 'Rylcev Alexy'


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('name', 'phone', 'city', 'text')


class TicketChangeForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
