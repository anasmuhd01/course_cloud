from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from instrctor.models import User

class InstructorForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']