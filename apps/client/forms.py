# coding=utf-8
from django import forms
from apps.city.models import City
from apps.client.models import Client, ClientMaket, ClientOrder, ClientJournal
from apps.manager.models import Manager
from core.models import User

__author__ = 'alexy'


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = []
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control hide'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'bik': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.TextInput(attrs={'class': 'form-control'}),
            'account_cor': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_post_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_name_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_doc_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_additional': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ClientUpdateForm, self).__init__(*args, **kwargs)
        user = self.request.user
        if self.request.user.type == 6:
            self.fields['city'].queryset = user.superviser.city.all()
            self.fields['manager'].queryset = Manager.objects.filter(moderator__in=user.superviser.moderator_id_list())
        elif user.type == 2:
            self.fields['city'].queryset = City.objects.filter(moderator=user)
            self.fields['manager'].queryset = Manager.objects.filter(moderator=user)
        elif user.type == 5:
            self.fields['city'].queryset = City.objects.filter(moderator=user.manager.moderator)
            if user.is_leader_manager():
                self.fields['manager'].queryset = Manager.objects.filter(moderator=user.manager.moderator)
            else:
                self.fields['manager'].queryset = Manager.objects.filter(user=user.manager.moderator)


class ClientAddForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['user', ]
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'bik': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.TextInput(attrs={'class': 'form-control'}),
            'account_cor': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_post_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_name_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_doc_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ClientAddForm, self).__init__(*args, **kwargs)
        user = self.request.user
        if user.type == 6:
            self.fields['manager'].queryset = Manager.objects.filter(moderator__in=user.superviser.moderator_id_list())
            self.fields['city'].queryset = user.superviser.city.all()
        elif user.type == 2:
            self.fields['manager'].queryset = Manager.objects.filter(moderator=user)
            self.fields['city'].queryset = City.objects.filter(moderator=user)
        elif user.type == 5:
            self.fields['city'].queryset = City.objects.filter(moderator=user.manager.moderator)
            if user.is_leader_manager():
                self.fields['manager'].queryset = Manager.objects.filter(moderator=user.manager.moderator)
            else:
                self.fields['manager'].queryset = Manager.objects.filter(user=user)
                self.fields['manager'].initial = user.manager


class ClientMaketForm(forms.ModelForm):
    class Meta:
        model = ClientMaket
        fields = ('client', 'name', 'file', 'date')
        widgets = {
            'client': forms.HiddenInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }


class ClientOrderForm(forms.ModelForm):
    class Meta:
        model = ClientOrder
        fields = ('client', 'date_start', 'date_end', 'name')
        widgets = {
            'client': forms.HiddenInput(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'name': forms.DateInput(attrs={'class': 'form-control'}),
        }


class ClientJournalForm(forms.ModelForm):
    class Meta:
        model = ClientJournal
        fields = ('client', 'clientorder', 'cost', 'add_cost', 'discount')
        widgets = {
            'client': forms.HiddenInput(attrs={'class': 'form-control'}),
            'clientorder': forms.CheckboxSelectMultiple(),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'add_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ClientJournalForm, self).__init__(*args, **kwargs)
        if self.initial:
            if 'client' in self.initial:
                client = self.initial['client']
                self.fields['clientorder'].queryset = client.clientorder_set.filter(is_closed=False)
