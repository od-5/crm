# coding=utf-8
from django import forms
from apps.adjuster.models import SurfacePhoto
from apps.city.models import Surface, City, Street, Porch, ManagementCompany
from apps.manager.models import Manager

__author__ = 'alexy'


class SurfaceImportForm(forms.Form):
    file = forms.FileField(label=u'Выберите файл', widget=forms.FileInput(attrs={'class': 'btn btn-default form-control'}))


class SurfaceAddForm(forms.ModelForm):
    class Meta:
        model = Surface
        fields = ('city', 'street', 'house_number', 'management')
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'street': forms.Select(attrs={'class': 'form-control'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control'}),
            'management': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Ограничение выбора города в зависимости от уровня доступа пользователя.
        Администратор может создавать поверхности для всех городов.
        Модератор - только для своих городов, руководитель группы - только для городов модератора
        """
        super(SurfaceAddForm, self).__init__(*args, **kwargs)
        initial = kwargs.pop('initial')
        user = initial['user']
        if user.type == 6:
            self.fields['city'].queryset = user.superviser.city.all()
            self.fields['street'].queryset = Street.objects.filter(city__in=user.superviser.city_id_list())
            self.fields['management'].queryset = ManagementCompany.objects.filter(city__in=user.superviser.city_id_list())
        elif user.type == 2:
            self.fields['city'].queryset = City.objects.filter(moderator=user)
            self.fields['street'].queryset = Street.objects.filter(city__moderator=user)
            self.fields['management'].queryset = ManagementCompany.objects.filter(city__moderator=user)
        elif user.type == 5:
            manager = Manager.objects.get(user=user)
            self.fields['city'].queryset = City.objects.filter(moderator=manager.moderator)
            self.fields['street'].queryset = Street.objects.filter(city__moderator=manager.moderator)
            self.fields['management'].queryset = ManagementCompany.objects.filter(city__moderator=manager.moderator)


class SurfacePhotoForm(forms.ModelForm):
    class Meta:
        model = SurfacePhoto
        fields = ('porch', 'date', 'image')
        widgets = {
            'porch': forms.HiddenInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PorchAddForm(forms.ModelForm):
    class Meta:
        model = Porch
        fields = ('surface', 'number', 'broken_shield', 'broken_gib', 'no_glass', 'replace_glass', 'against_tenants',
                  'no_social_info')
        widgets = {
            'surface': forms.HiddenInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'broken_shield': forms.CheckboxInput(),
            'broken_gib': forms.CheckboxInput(),
            'no_glass': forms.CheckboxInput(),
            'replace_glass': forms.CheckboxInput(),
            'against_tenants': forms.CheckboxInput(),
            'no_social_info': forms.CheckboxInput(),
        }
