# coding=utf-8
from django import forms
from apps.adjuster.models import Adjuster
from apps.city.models import City

__author__ = 'alexy'


class AdjusterAddForm(forms.ModelForm):
    class Meta:
        model = Adjuster
        exclude = ['user', ]
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdjusterAddForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)


class AdjusterUpdateForm(forms.ModelForm):
    class Meta:
        model = Adjuster
        exclude = []
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control hide'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdjusterUpdateForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)


class AdjusterPaymentForm(forms.ModelForm):
    class Meta:
        model = Adjuster
        fields = ('cost_mounting', 'cost_change', 'cost_repair', 'cost_dismantling')
        widgets = {
            'cost_mounting': forms.TextInput(attrs={'class': 'form-control'}),
            'cost_change': forms.TextInput(attrs={'class': 'form-control'}),
            'cost_repair': forms.TextInput(attrs={'class': 'form-control'}),
            'cost_dismantling': forms.TextInput(attrs={'class': 'form-control'}),
        }
