# coding=utf-8
from django.forms import ModelForm, TextInput, Select, DateInput, inlineformset_factory
from django import forms
from .models import City, Surface, Area, Porch

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


class SurfaceAddForm(ModelForm):
    class Meta:
        model = Surface
        fields = ('city', 'area', 'street', 'house_number')
        widgets = {
            'city': Select(attrs={'class': 'form-control'}),
            'area': Select(attrs={'class': 'form-control'}),
            'street': TextInput(attrs={'class': 'form-control'}),
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
            self.fields['area'].queryset = Area.objects.filter(city__moderator=user)

PorchFormSet = inlineformset_factory(Surface, Porch, extra=3, can_delete=True, exclude=[])
