from django.shortcuts import render
from django.views import View
# Create your views here.

class SigninView(View):
    def get(self,req):
        return render(req,'studentsignup.html')

class SignupView(View):
    def get(self,req):
        return render(req,'signup.html')