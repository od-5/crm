# coding=utf-8
from django import forms
from core.models import User
from .models import IncomingClient, IncomingTask, IncomingClientContact

__author__ = 'alexy'


class IncomingClientImportForm(forms.Form):
    file = forms.FileField(label=u'Выберите файл', widget=forms.FileInput(attrs={'class': 'btn btn-default form-control'}))


class IncomingClientAddForm(forms.ModelForm):
    class Meta:
        model = IncomingClient
        fields = '__all__'
        exclude = ['type', ]
        widgets = {
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kind_of_activity': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_address': forms.TextInput(attrs={'class': 'form-control'}),
            'site': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # todo: сделать проверку на уникальнось комбинации data[name] и data[city]
    def clean_name(self):
        data = self.cleaned_data
        try:
            IncomingClient.objects.get(name=data['name'])
        except IncomingClient.DoesNotExist:
            return data['name']
        raise forms.ValidationError(u'Клиент с таким названием уже есть в системе')


class IncomingClientUpdateForm(forms.ModelForm):
    class Meta:
        model = IncomingClient
        exclude = ['type', ]
        widgets = {
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kind_of_activity': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_address': forms.TextInput(attrs={'class': 'form-control'}),
            'site': forms.TextInput(attrs={'class': 'form-control'}),
        }


class IncomingClientContactForm(forms.ModelForm):
    class Meta:
        model = IncomingClientContact
        fields = '__all__'
        widgets = {
            'incomingclient': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'function': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


class IncomingTaskForm(forms.ModelForm):
    class Meta:
        model = IncomingTask
        fields = '__all__'
        widgets = {
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'incomingclient': forms.Select(attrs={'class': 'form-control'}),
            'incomingclientcontact': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': u'Текст комментария к задаче'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }
