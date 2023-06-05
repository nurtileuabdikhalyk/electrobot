from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Contact, Order


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'message')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('city', 'street', 'house', 'house_number')
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control', }),
            'street': forms.TextInput(attrs={'class': 'form-control', }),
            'house': forms.NumberInput(attrs={'class': 'form-control', }),
            'house_number': forms.NumberInput(attrs={'class': 'form-control', }),
        }


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Есіміңіз"}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Тегіңіз"}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Логин"}))

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Құпия сөз"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Құпия сөзді қайталаңыз"}))

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+7 707 000 00 00"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'phone')


class LoginForm(forms.ModelForm):
    login = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Логин"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Құпия сөз"}))

    class Meta:
        model = User
        fields = ('login', 'password',)
