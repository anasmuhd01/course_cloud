from django import forms
from django.contrib.auth.forms import UserCreationForm
from instrctor.models import User

class StudentCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','username','password1','password2']

class SigninForm(forms.Form ):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

