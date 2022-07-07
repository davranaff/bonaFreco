from django import forms
from .models import Order
from captcha.fields import *


class CrateOrder(forms.ModelForm):
    address = forms.CharField(help_text='address', widget=forms.TextInput(attrs={'class': 'input', 'name': 'address'}))
    telephone_number = forms.IntegerField(help_text='number',
                                          widget=forms.TextInput(attrs={'class': 'input', 'name': 'telephone_number'}))
    captcha = CaptchaField(label='Enter text from image',
                           error_messages={'invalid': 'Wrong text'})

    class Meta:
        model = Order
        fields = ['address', 'telephone_number']
