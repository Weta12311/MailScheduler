from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from mailing.mixins import StyleFormMixin
from users.models import User


class UserAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "validate"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "validate"})
    )


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "validate"}),
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "validate"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "validate"}),
    )

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class UserProfileForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
