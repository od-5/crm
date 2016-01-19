# coding=utf-8
from django import forms
from apps.adjuster.models import SurfacePhoto
from apps.city.models import Surface, City, Street, Porch
from apps.client.models import ClientSurface

__author__ = 'alexy'


class SurfaceAddForm(forms.ModelForm):
    class Meta:
        model = Surface
        fields = ('city', 'street', 'house_number')
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'street': forms.Select(attrs={'class': 'form-control'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control'}),
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


class SurfacePhotoForm(forms.ModelForm):
    class Meta:
        model = SurfacePhoto
        fields = ('porch', 'date', 'image')
        widgets = {
            'porch': forms.HiddenInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class SurfaceClientAddForm(forms.ModelForm):
    class Meta:
        model = ClientSurface
        fields = ('client', 'surface', 'date_start', 'date_end')
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'surface': forms.HiddenInput(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control'}),
        }


class PorchAddForm(forms.ModelForm):
    class Meta:
        model = Porch
        fields = ('surface', 'number', 'broken_shield', 'broken_gib', 'no_glass', 'replace_glass', 'against_tenants',
                  'no_social_info')
        widgets = {
            'surface': forms.HiddenInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'broken_shield': forms.TextInput(attrs={'class': 'form-control'}),
            'broken_gib': forms.TextInput(attrs={'class': 'form-control'}),
            'no_glass': forms.TextInput(attrs={'class': 'form-control'}),
            'replace_glass': forms.TextInput(attrs={'class': 'form-control'}),
            'against_tenants': forms.TextInput(attrs={'class': 'form-control'}),
            'no_social_info': forms.TextInput(attrs={'class': 'form-control'}),
        }
