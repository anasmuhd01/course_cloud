from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,FormView,CreateView
from student.forms import *
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from django.contrib import messages


# django generic views
class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = StudentCreationForm
    success_url = reverse_lazy('signin')
    # def form_invalid(self, form):
    #     messages.warning(self.request,"Invalid Username/password")
    #     return redirect('signin')



class CCHomeView(View):
    def get(self,req):
        return render(req,'homepage.html')


class SigninView(FormView):
    form_class = SigninForm
    template_name = 'studentsignin.html'

    
    def post(self,req):
        form_data = SigninForm(data=req.POST)

        if form_data.is_valid():
            # the same can be used like
            # uname = form_data.cleaned_data['username']
            uname = form_data.cleaned_data.get('username')
            pswd = form_data.cleaned_data.get('password') 
            user = authenticate(req,username = uname, password = pswd)
            if user:
                if user.role == 'Student':
                    login(req,user)
                    return redirect('cchome')
                if user.role == 'Instructor':
                    login(req,user)
                    return redirect('admin:index')

            else:
                messages.warning(req,'Invalid username/password')
                return redirect('signin')
        

class LogoutView(View):
    def get(self,req):
        logout(req)
        return redirect('signin')
