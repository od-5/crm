# coding=utf-8
from django import forms
from apps.adjuster.models import Adjuster, AdjusterTask
from apps.city.models import City, Surface, Area
from apps.client.models import Client, ClientOrder
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
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': u'Текст комментария к задаче'}),
        }

    client = forms.ModelChoiceField(queryset=Client.objects.all(), label=u'Клиент', widget=forms.Select(attrs={'class': 'form-control'}))
    # clientorder = forms.ChoiceField(choices=((0, '---------'),), label=u'Заказ', widget=forms.Select(attrs={'class': 'form-control'}))

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
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': u'Текст комментария к задаче'}),
        }

    city = forms.ModelChoiceField(queryset=City.objects.all(), label=u'Город', widget=forms.Select(attrs={'class': 'form-control'}))
    area = forms.ModelChoiceField(queryset=Area.objects.all(), label=u'Район', widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdjusterTaskAddForm, self).__init__(*args, **kwargs)
        if self.request.user and self.request.user.type == 2:
            self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)
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


class AdjusterTaskFilterForm(forms.Form):
    TYPE_CHOICES = (
        (None, u'---------'),
        (0, u'Монтаж новой конструкции'),
        (1, u'Замена'),
        (2, u'Ремонт стенда'),
        (3, u'Демонтаж стенда'),
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label=u'Город',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    adjuster = forms.ModelChoiceField(
        queryset=Adjuster.objects.all(),
        label=u'Монтажник',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        label=u'Тип работы',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_s = forms.DateField(
        label=u'Дата от',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    date_e = forms.DateField(
        label=u'до',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
