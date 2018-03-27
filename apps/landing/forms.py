# coding=utf-8
from django import forms

from apps.city.models import City
from .models import Setup, BlockExample, BlockReview, BlockEffective

__author__ = 'alexy'


class SetupForm(forms.ModelForm):
    class Meta:
        model = Setup
        fields = '__all__'
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'logotype': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_keys': forms.Textarea(attrs={'class': 'form-control'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'video_find': forms.TextInput(attrs={'class': 'form-control'}),
            'top_js': forms.Textarea(attrs={'class': 'form-control'}),
            'bottom_js': forms.Textarea(attrs={'class': 'form-control'}),
            'robots_txt': forms.Textarea(attrs={'class': 'form-control'}),
            'video': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SetupForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['city'].queryset = City.objects.get_qs(user)
            if user.type != 1 or self.instance.city_id:
                self.fields['top_js'].widget = forms.HiddenInput()
                self.fields['bottom_js'].widget = forms.HiddenInput()
                self.fields['robots_txt'].widget = forms.HiddenInput()


class BlockEffectiveForm(forms.ModelForm):
    class Meta:
        model = BlockEffective
        fields = '__all__'
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class BlockExampleForm(forms.ModelForm):
    class Meta:
        model = BlockExample
        fields = '__all__'
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class BlockReviewForm(forms.ModelForm):
    class Meta:
        model = BlockReview
        fields = '__all__'
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }

