# store/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Order  # Import your models here

# User Registration Form
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat Password')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        """Ensure the two password entries match."""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

# User Login Form
class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

# Profile Update Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

# Checkout Form
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order  # Assuming 'Order' is a model representing orders in your app
        fields = ['address', 'city', 'postal_code', 'country']
