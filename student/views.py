from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,FormView,CreateView
from student.forms import *
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate

# Create your views here.

# the same view can be done using templateview
# class SigninView(View):
#     def get(self,req):
#         return render(req,'studentsignup.html')

# class SigninView(TemplateView):
#     template_name =  'studentsignin.html'

# class SignupView(View):
#     def get(self,req):
#         return render(req,'signup.html')

# using TemplateView



# class SignupView(TemplateView):
#     template_name = 'signup.html'
#     form_class = StudentCreationForm

class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = StudentCreationForm
    success_url = reverse_lazy('signin')



class SigninView(View):
    def get(self,req):
        form = SigninForm()

        return render(req,'studentsignin.html')
    def post(self,req):
        form_data = SigninForm(req.POST)
        username = req.POST.get('username')
        print(username)
