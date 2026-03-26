from django import forms
from django.contrib.auth import get_user_model

User= get_user_model()

class RegisterForm(forms.Moels):
    password= forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model= User
        fields= ['username','email','password','role']

class LoginForm(forms.Form):
    username= forms.CharField()
    password= forms.CharField(widget=forms.PasswordInput)