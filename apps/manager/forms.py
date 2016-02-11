# coding=utf-8
from django import forms
from .models import Manager
from core.models import User

__author__ = 'alexy'


# class ClientUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         exclude = []
#         widgets = {
#             'user': forms.Select(attrs={'class': 'form-control hide'}),
#             'city': forms.Select(attrs={'class': 'form-control'}),
#             'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'actual_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'inn': forms.TextInput(attrs={'class': 'form-control'}),
#             'kpp': forms.TextInput(attrs={'class': 'form-control'}),
#             'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
#             'bank': forms.TextInput(attrs={'class': 'form-control'}),
#             'bik': forms.TextInput(attrs={'class': 'form-control'}),
#             'account': forms.TextInput(attrs={'class': 'form-control'}),
#             'account_cor': forms.TextInput(attrs={'class': 'form-control'}),
#             'signer_post_dec': forms.TextInput(attrs={'class': 'form-control'}),
#             'signer_name_dec': forms.TextInput(attrs={'class': 'form-control'}),
#             'signer_doc_dec': forms.TextInput(attrs={'class': 'form-control'}),
#             'legal_address': forms.TextInput(attrs={'class': 'form-control'}),
#             'leader': forms.TextInput(attrs={'class': 'form-control'}),
#             'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
#             'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop("request")
#         super(ClientUpdateForm, self).__init__(*args, **kwargs)
#         if self.request.user and self.request.user.type == 2:
#             self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)


class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        exclude = ['user', ]
        widgets = {
            'moderator': forms.Select(attrs={'class': 'form-control'}),
        }
