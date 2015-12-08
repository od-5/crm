from django.forms import ModelForm
from core.models import User

__author__ = 'alexy'


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name',)