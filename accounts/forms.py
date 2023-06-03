from typing import Any
from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def clean_password2(self):
        password1, password2 = self.cleaned_data['password1'], self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError('Password must be matches')

        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='<a href="../password/">change password </a>')

    class Meta:
        model = User
        fields = ('email', 'password', 'full_name',
                  'last_login', 'is_active', 'is_admin')


class UserCreateForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        password1, password2 = self.cleaned_data['password1'], self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError('Password must be matches')

        return password1

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number)
        if user.exists:
            raise ValidationError('this phone number already exists')
        otp = OtpCode.objects.filter(phone_number=phone_number).delete()

        return phone_number


class OtpCodeForm(forms.Form):
    code = forms.IntegerField(min_value=10000, widget=forms.TextInput(
        attrs={'class': 'form-control'}))


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
