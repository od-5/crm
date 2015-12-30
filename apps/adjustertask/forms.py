# coding=utf-8
from django import forms
from apps.adjuster.models import Adjuster, AdjusterTask
from apps.city.models import City, Surface, Area
from apps.client.models import Client
from core.models import User

__author__ = 'alexy'


class AdjusterTaskClientAddForm(forms.ModelForm):
    class Meta:
        model = AdjusterTask
        fields = ('adjuster', 'type', 'date', 'comment')
        widgets = {
            'adjuster': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control '}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

    client = forms.ModelChoiceField(queryset=Client.objects.all(), label=u'Клиент', widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdjusterTaskClientAddForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['adjuster'].queryset = Adjuster.objects.filter(city__moderator=self.request.user)
            self.fields['client'].queryset = Client.objects.filter(city__moderator=self.request.user)


class AdjusterTaskAddForm(forms.ModelForm):
    class Meta:
        model = AdjusterTask
        fields = ('adjuster', 'type', 'date', 'comment')
        widgets = {
            'adjuster': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control at_date'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

    area = forms.ModelChoiceField(queryset=Surface.objects.all(), label=u'Район', widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdjusterTaskAddForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['adjuster'].queryset = Adjuster.objects.filter(city__moderator=self.request.user)
            self.fields['area'].queryset = Area.objects.filter(city__moderator=self.request.user)


class AdjusterTaskUpdateForm(forms.ModelForm):
    class Meta:
        model = AdjusterTask
        fields = ('adjuster', 'type', 'date', 'comment')
        widgets = {
            'adjuster': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdjusterTaskUpdateForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['adjuster'].queryset = Adjuster.objects.filter(city__moderator=self.request.user)
