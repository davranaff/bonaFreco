from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from captcha.fields import CaptchaField


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(help_text='you\'r first name',
                                 error_messages={'invalid': 'поле неправильно заполнено'},
                                 widget=forms.TextInput(attrs={'class': 'input my-3', 'placeholder': 'write here...'}))
    last_name = forms.CharField(help_text='you\'r last name', error_messages={'invalid': 'поле неправильно заполнено'},
                                widget=forms.TextInput(attrs={'class': 'input my-3', 'placeholder': 'write here...'}))
    username = forms.CharField(help_text='you\'r username', error_messages={'invalid': 'поле неправильно заполнено'},
                               widget=forms.TextInput(attrs={'class': 'input my-3', 'placeholder': 'write here...'}))
    email = forms.EmailField(help_text='you\'r mail', error_messages={'invalid': 'поле неправильно заполнено'},
                             widget=forms.EmailInput(attrs={'class': 'input my-3', 'placeholder': 'write here...'}))
    password1 = forms.CharField(help_text='you\'r password', error_messages={'invalid': 'поле неправильно заполнено'},
                                widget=forms.PasswordInput(
                                    attrs={'class': 'input my-3', 'placeholder': 'write here...'}))
    password2 = forms.CharField(help_text='confirm password', error_messages={'invalid': 'поле неправильно заполнено'},
                                widget=forms.PasswordInput(
                                    attrs={'class': 'input my-3', 'placeholder': 'write here...'}))
    captcha = CaptchaField(label='Enter text from image',
                           error_messages={'invalid': 'Wrong text'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(help_text='you\'r old password',
                                   error_messages={'invalid': 'поле неправильно заполнено'}, widget=forms.PasswordInput(
            attrs={'class': 'input my-3', 'placeholder': 'old password'}))
    new_password1 = forms.CharField(help_text='you\'r new password',
                                    error_messages={'invalid': 'поле неправильно заполнено'},
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'input my-3', 'placeholder': 'new password'}))
    new_password2 = forms.CharField(help_text='retry new password',
                                    error_messages={'invalid': 'поле неправильно заполнено'},
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'input my-3', 'placeholder': 'confirm new password'}))
    captcha = CaptchaField(label='Enter text from image',
                           error_messages={'invalid': 'Wrong text'})

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
