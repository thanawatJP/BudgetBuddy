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
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            msg = "Your email have been use"
            self.add_error("email", msg)

        return email

class ResetpasswordForm(SetPasswordForm):
    # email = forms.CharField()

    class Meta:
        model = User
        fields = [
            "email",
            "username",
        ]