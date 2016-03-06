# coding=utf-8
from django import forms
from core.models import User, Setup, BlockEffective, BlockExample, BlockReview

__author__ = 'alexy'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name',)


class UserAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'patronymic', 'phone')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    password1 = forms.CharField(label=u'Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        data = self.cleaned_data
        try:
            User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return data['email']
        raise forms.ValidationError(u'Пользователь с таким e-mail уже зарегистрирован')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'Пароль и подтверждение пароля не совпадают!')
        return password2

    def save(self, commit=True):
        user = super(UserAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'patronymic', 'phone')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ModeratorAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'patronymic', 'phone', 'company', 'leader', 'leader_function', 'work_basis')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
        }

    password1 = forms.CharField(label=u'Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        data = self.cleaned_data
        try:
            User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return data['email']
        raise forms.ValidationError(u'Пользователь с таким e-mail уже зарегистрирован')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'Пароль и подтверждение пароля не совпадают!')
        return password2

    def save(self, commit=True):
        user = super(ModeratorAddForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ModeratorUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name', 'patronymic', 'phone', 'company', 'leader', 'leader_function', 'work_basis')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SetupForm(forms.ModelForm):
    class Meta:
        model = Setup
        fields = '__all__'
        widgets = {
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_keys': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_desc': forms.TextInput(attrs={'class': 'form-control'}),
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
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class BlockExampleForm(forms.ModelForm):
    class Meta:
        model = BlockExample
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class BlockReviewForm(forms.ModelForm):
    class Meta:
        model = BlockReview
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
