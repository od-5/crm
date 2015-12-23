# coding=utf-8
from django.contrib import admin
from django.forms import ModelForm
from core.models import User
from .models import Client, ClientMaket

__author__ = 'alexy'


class ClientMaketInline(admin.TabularInline):
    model = ClientMaket
    extra = 1


class ClientAdminForm(ModelForm):
    model = Client
    exclude = []

    def __init__(self, *args, **kwargs):
        super(ClientAdminForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(type=3)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'legal_name', 'actual_name', 'leader')
    form = ClientAdminForm
    inlines = [
        ClientMaketInline
    ]

admin.site.register(Client, ClientAdmin)
