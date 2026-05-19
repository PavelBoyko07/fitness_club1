from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Application, Review


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('client_name', 'phone_number', 'payment_type')
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Введите имя'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': '+371 2000 0000'
            }),
            'payment_type': forms.Select(attrs={
                'class': 'form-select rounded-pill'
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('author_name', 'rating', 'text')
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Ваше имя'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control rounded-pill',
                'min': 1,
                'max': 5,
                'placeholder': 'Оценка от 1 до 5'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control rounded-4',
                'rows': 4,
                'placeholder': 'Ваш отзыв'
            }),
        }


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='',
        help_text='Только буквы, цифры и символы @/./+/-/_',
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите логин'
        })
    )
    email = forms.EmailField(
        label='',
        help_text='Введите настоящий email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите email'
        })
    )
    password1 = forms.CharField(
        label='',
        help_text='Минимум 8 символов',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите пароль'
        })
    )
    password2 = forms.CharField(
        label='',
        help_text='Повторите пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-pill',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите логин'
        })
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите пароль'
        })
    )
