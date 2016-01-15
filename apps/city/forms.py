# coding=utf-8
from django.forms import ModelForm, TextInput, Select, DateInput, inlineformset_factory, FileInput, HiddenInput, \
    modelformset_factory
from apps.adjuster.models import SurfacePhoto
from apps.client.models import ClientSurface
from core.models import User
from .models import City, Surface, Porch, Street, Area

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


PorchFormSet = inlineformset_factory(Surface, Porch, extra=1, can_delete=True, exclude=[])
AreaModelFormset = modelformset_factory(Area, form=AreaAddForm)
