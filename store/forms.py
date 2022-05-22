from django import forms
from django.contrib.auth.forms import authenticate
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("invalid log in credentials")


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address')
    name = forms.CharField(max_length=60)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text='Password must contain at least 8 charecter including numeric values',
    )

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2")


class CheckoutForm(ModelForm):

    address = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = Delivery
        fields = ("address", "phone")

    def clean(self):
        if self.is_valid():
            address = self.cleaned_data.get('address')
            phone = self.cleaned_data.get('phone')





