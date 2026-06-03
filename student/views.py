from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,FormView,CreateView,ListView,DetailView
from student.forms import *
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from django.contrib import messages
from instrctor.models import Course
from student.models import Cart,Course,Wishlist


# django generic views
class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = StudentCreationForm
    success_url = reverse_lazy('signin')
    # def form_invalid(self, form):
    #     messages.warning(self.request,"Invalid Username/password")
    #     return redirect('signin')



class CCHomeView(ListView):
    template_name = 'homepage.html'
    queryset = Course.objects.all()
    context_object_name = 'courses'


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


class CourseDetailsView(DetailView):
    template_name = 'coursedetails.html'
    queryset = Course.objects.all()
    pk_url_kwarg = 'cid'
    context_object_name = 'course'


class AddtoCart(View):
    def get(self,req,**kwargs):
        id = kwargs.get('id')
        course = Course.objects.get(id=id)
        student = req.user
        (object,created) = Cart.objects.get_or_create(course_object=course,student_object=student)
        if created:
            return redirect('cchome')
        else:
            messages.warning(req,'Already added to cart')
            return redirect('cchome')
        

class CartlistView(View):
    def get(self,req):
        cartlist = Cart.objects.filter(student_object = req.user)
        cart_count = cartlist.count()
        total = 0
        for i in cartlist:
            total += i.course_object.price
        return render(req,'cartlist.html',{'data':cartlist,'count':cart_count,'price':total})
    
class DeleteCartItemView(View):
    def get(self,req,**kwargs):
        cid = kwargs.get('id')
        Cart.objects.get(id=cid).delete()
        return redirect('cartlist')
    

class WishlistView(View):
    def get(self,req,**kwargs):

        id = kwargs.get('id')
        course = Course.objects.get(id=id)
        student = req.user
        (object,created) = Wishlist.objects.get_or_create(course_object = course,student_object = student)
        
        if created:
            return redirect('cchome')
        else:
            messages.warning(req,'In Wishlist')
            return redirect('cchome')
        
class WishlistAllView(View):
    def get(self,req):
        print(Wishlist.objects.filter(student_object=req.user).count())
        data = Wishlist.objects.filter(student_object = req.user)
        return render(req,'wishlist.html',{'wishlist':data})
    
class DeleteWishlistView(View):
    def get(self,req,**kwargs):
        id = kwargs.get('id')
        Wishlist.objects.get(id=id).delete()
        return redirect('wishlistall')