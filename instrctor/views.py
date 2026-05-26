from django.shortcuts import render,redirect
from instrctor.forms import InstructorForm
from django.views import View
# Create your views here.

class InstructorSignupView(View):
    def get(self,req):
        form = InstructorForm()
        return render(req, 'inssignup.html',{'form':form})
    
    def post(self,req):
        form_data = InstructorForm(data=req.POST)
        if form_data.is_valid():
            instructor = form_data.save(commit=False)
            instructor.is_superuser = True
            instructor.is_staff = True
            instructor.role = "Instructor"
            instructor.save()
            return redirect('inssignup')

