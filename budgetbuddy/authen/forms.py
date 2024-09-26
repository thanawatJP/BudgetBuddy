from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.forms import ModelForm
from django.contrib.auth.models import User

class RegisterationForm(UserCreationForm):
    # email = forms.EmailField()
    
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password1",
            "password2",
        ]

class ResetpasswordForm(SetPasswordForm):
    # email = forms.CharField()

    class Meta:
        model = User
        fields = [
            "email",
            "username",
        ]