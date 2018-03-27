# coding=utf-8
from django import forms

from apps.city.models import City
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TicketChangeForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['city'].queryset = City.objects.get_qs(user)
