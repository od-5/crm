# coding=utf-8
from django import forms
from .models import Setup, BlockExample, BlockReview, BlockEffective

__author__ = 'alexy'


class SetupForm(forms.ModelForm):
    class Meta:
        model = Setup
        fields = '__all__'
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_keys': forms.Textarea(attrs={'class': 'form-control'}),
            'meta_desc': forms.Textarea(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'top_js': forms.Textarea(attrs={'class': 'form-control'}),
            'bottom_js': forms.Textarea(attrs={'class': 'form-control'}),
            'robots_txt': forms.Textarea(attrs={'class': 'form-control'}),
            'video': forms.Textarea(attrs={'class': 'form-control'}),
        }


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

