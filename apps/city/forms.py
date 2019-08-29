# coding=utf-8
from django import forms
from .models import City, Street, Area, ManagementCompany

__author__ = 'alexy'


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name', 'moderator', 'contract_number', 'contract_date', 'slug', 'timezone',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'moderator': forms.Select(attrs={'class': 'form-control'}),
            'contract_number': forms.TextInput(attrs={'class': 'form-control'}),
            'contract_date': forms.DateInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'timezone': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = None
        if 'user' in kwargs:
            user = kwargs.pop('user')
        super(CityForm, self).__init__(*args, **kwargs)
        if user and user.type != 1:
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = True


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ('city', 'name', )
        widgets = {
            'city': forms.HiddenInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Название района'}),
        }


class StreetForm(forms.ModelForm):
    class Meta:
        model = Street
        fields = ('city', 'area', 'name')
        widgets = {
            'city': forms.HiddenInput(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop("request")
        super(StreetForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['area'].queryset = self.instance.city.area_set.all()
        else:
            self.fields['area'].queryset = self.initial['city'].area_set.all()


class ManagementCompanyForm(forms.ModelForm):
    class Meta:
        model = ManagementCompany
        fields = '__all__'
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'phones': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ManagementCompanyForm, self).__init__(*args, **kwargs)
        if self.request.user:
            if self.request.user.type == 6:
                self.fields['city'].queryset = self.request.user.superviser.city.all()
            elif self.request.user.type == 2:
                self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)

    def clean_phones(self):
        value = self.cleaned_data['phones']
        for phone in value.split('$'):
            if phone and len(phone.split('#')) != 2:
                raise forms.ValidationError('Неверный формат')
        return value
