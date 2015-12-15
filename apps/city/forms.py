# coding=utf-8
from django.forms import ModelForm, TextInput, Select, DateInput, inlineformset_factory
from django import forms
from core.models import User
from .models import City, Surface, Area, Porch, Street

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


class SurfaceAddForm(ModelForm):
    class Meta:
        model = Surface
        fields = ('city', 'street', 'house_number')
        widgets = {
            'city': Select(attrs={'class': 'form-control'}),
            'street': Select(attrs={'class': 'form-control'}),
            'house_number': TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Ограничение выбора города в зависимости от ровня доступа пользователя.
        Администратор может создавать поверхности для всех городов.
        Модератор - только для своих городов
        """
        super(SurfaceAddForm, self).__init__(*args, **kwargs)
        initial = kwargs.pop('initial')
        user = initial['user']
        if user.type == 2:
            self.fields['city'].queryset = City.objects.filter(moderator=user)
            self.fields['street'].queryset = Street.objects.filter(city__moderator=user)

PorchFormSet = inlineformset_factory(Surface, Porch, extra=3, can_delete=True, exclude=[])


class StreetForm(ModelForm):
    class Meta:
        model = Street
        fields = ('city', 'area', 'name')
        widgets = {
            'city': Select(attrs={'class': 'form-control'}),
            'area': Select(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
        }
