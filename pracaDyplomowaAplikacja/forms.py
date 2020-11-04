from django.forms import ModelForm
from .models import Przepis
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PrzepisForm(ModelForm):
    class Meta:
        model = Przepis
        fields = ['nazwa','opis','zdjecie','czas_przygotowania','stopien_trudnosci']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']