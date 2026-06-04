from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,FormView,CreateView,ListView,DetailView
from student.forms import *
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from django.contrib import messages
from instrctor.models import Course
from student.models import Cart,Course,Wishlist,Order
import razorpay
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Razorpay keys 
RAZORPAY_KEY = "rzp_test_SxQtLPRLPQ08jd"
RAZORPAY_SECRET_KEY = "9Xk2z1fJQVK7X4MyVVxQVXO1"


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
    

class PlaceOrderView(View):
    def get(self,req):
        student = req.user
        qs = Cart.objects.filter(student_object = student)
        
        cart_total = 0
        for i in qs:
            cart_total += i.course_object.price
        order = Order.objects.create(student_object = student,total =cart_total)
        for i in qs:
            order.course_object.add(i.course_object)
        qs.delete()

        if cart_total > 0:
            print('payment gateway')
            client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET_KEY))

            data = { "amount": int(cart_total), "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data) 
            print(payment)
            order.razr_pay_id = payment.get('id')
            order.save()
            context = {
                'razor_pay_key':RAZORPAY_KEY,
                'amount':int(cart_total),
                'razr_pay_id':payment.get('id')
            }
            return render(req,'payment.html',{'data':context})


        elif cart_total == 0 :
            order.is_paid = True
            order.save()
            return redirect('cchome')

        else:
            return redirect('cchome')
        
@method_decorator(csrf_exempt,name="dispatch")
class Paymentview(View):
    def post(self,req):
        print(req.POST)
        print(req.POST.get('razorpay_order_id'))
        client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET_KEY))
        try:
            client.utility.verify_payment_signature(req.POST)
            razr_pay_id = req.POST.get('razorpay_order_id')  
            order = Order.objects.get(razr_pay_id=razr_pay_id)
            order.is_paid = True
            order.save()
        except:
            print('Failed')

        return redirect('cchome')
    

class MycourseView(View):
    def get(self,req):
        order_qs = Order.objects.filter(is_paid=True,student_object=req.user)
        return render(req,'mycourse.html',{'dat':order_qs})


        
