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
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ClientUpdateForm, self).__init__(*args, **kwargs)
        if self.request.user:
            if self.request.user.type == 6:
                self.fields['city'].queryset = self.request.user.superviser.city.all()
                self.fields['manager'].queryset = Manager.objects.filter(moderator__in=self.request.user.superviser.moderator_id_list())
            elif self.request.user.type == 2:
                self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)
                self.fields['manager'].queryset = Manager.objects.filter(moderator=self.request.user)
            elif self.request.user.type == 5 and self.request.user.is_leader_manager():
                manager = Manager.objects.get(user=self.request.user)
                self.fields['city'].queryset = City.objects.filter(moderator=manager.moderator)
                self.fields['manager'].queryset = Manager.objects.filter(moderator=manager.moderator)


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
        if self.request.user:
            if self.request.user.type == 6:
                self.fields['city'].queryset = self.request.user.superviser.city.all()
            if self.request.user.type == 2:
                self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)
            elif self.request.user.type == 5 and self.request.user.is_leader_manager():
                manager = Manager.objects.get(user=self.request.user)
                self.fields['city'].queryset = City.objects.filter(moderator=manager.moderator)


class ClientMaketForm(forms.ModelForm):
    class Meta:
        model = ClientMaket
        fields = ('client', 'name', 'file', 'date')
        widgets = {
            'client': forms.HiddenInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
        }


class ClientOrderForm(forms.ModelForm):
    class Meta:
        model = ClientOrder
        fields = ('client', 'date_start', 'date_end')
        widgets = {
            'client': forms.HiddenInput(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control'}),
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

