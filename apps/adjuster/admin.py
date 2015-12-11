# coding=utf-8
from django.contrib import admin
from django.forms import ModelForm
from core.models import User
from .models import Adjuster

__author__ = 'alexy'


class AdjusterAdminForm(ModelForm):
    model = Adjuster
    exclude = []

    def __init__(self, *args, **kwargs):
        super(AdjusterAdminForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(type=4)


class AdjusterAdmin(admin.ModelAdmin):
    list_display = ('user', 'city')
    form = AdjusterAdminForm

admin.site.register(Adjuster, AdjusterAdmin)
