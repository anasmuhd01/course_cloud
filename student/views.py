from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,FormView,CreateView,ListView,DetailView
from student.forms import *
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from django.contrib import messages
from instrctor.models import Course,Lesson,Module
from student.models import Cart,Course,Wishlist,Order
import razorpay
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from decouple import config

# Razorpay keys 
RAZORPAY_KEY = config('RAZORPAY_KEY')
RAZORPAY_SECRET_KEY = config('RAZORPAY_SECRET_KEY')


#sigin-decorator 
def signin_required(fn):
    def inner(req,*args,**kwargs):
        if req.user.is_authenticated:
            return fn(req,*args,**kwargs)
        else:
            return redirect('signin')
    return inner

# django generic views
class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = StudentCreationForm
    success_url = reverse_lazy('signin')
    # def form_invalid(self, form):
    #     messages.warning(self.request,"Invalid Username/password")
    #     return redirect('signin')


@method_decorator([signin_required,never_cache],name='dispatch')
class CCHomeView(ListView):
    template_name = 'homepage.html'
    queryset = Course.objects.all()
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchased_course = Order.objects.filter(student_object = self.request.user,is_paid=True).values_list('course_object',flat=True)
        context['purchased_course'] = purchased_course
        # print(context)
        return context

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

@method_decorator([signin_required,never_cache],name='dispatch')
class CourseDetailsView(DetailView):
    template_name = 'coursedetails.html'
    queryset = Course.objects.all()
    pk_url_kwarg = 'cid'
    context_object_name = 'course'

@method_decorator([signin_required,never_cache],name='dispatch')
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
        

@method_decorator([signin_required,never_cache],name='dispatch')
class CartlistView(View):
    def get(self,req):
        cartlist = Cart.objects.filter(student_object = req.user)
        cart_count = cartlist.count()
        total = 0
        for i in cartlist:
            total += i.course_object.price
        return render(req,'cartlist.html',{'data':cartlist,'count':cart_count,'price':total})

@method_decorator([signin_required,never_cache],name='dispatch')  
class DeleteCartItemView(View):
    def get(self,req,**kwargs):
        cid = kwargs.get('id')
        Cart.objects.get(id=cid).delete()
        return redirect('cartlist')
    
@method_decorator([signin_required,never_cache],name='dispatch')
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

# @method_decorator([signin_required,never_cache],name='dispatch')       
class WishlistAllView(View):
    def get(self,req):
        print(Wishlist.objects.filter(student_object=req.user).count())
        data = Wishlist.objects.filter(student_object = req.user)
        return render(req,'wishlist.html',{'wishlist':data})

@method_decorator([signin_required,never_cache],name='dispatch')
class DeleteWishlistView(View):
    def get(self,req,**kwargs):
        id = kwargs.get('id')
        Wishlist.objects.get(id=id).delete()
        return redirect('wishlistall')
    
@method_decorator([signin_required,never_cache],name='dispatch')
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

            data = { "amount": int(cart_total)*100, "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data) 
            print(payment)
            order.razr_pay_id = payment.get('id')
            order.save()
            context = {
                'razor_pay_key':RAZORPAY_KEY,
                'amount':int(cart_total),
                'razr_pay_id':payment.get('id')
            }
            print("cart_total =", cart_total)
            print(payment)
            return render(req,'payment.html',{'data':context})


        elif cart_total == 0 :
            order.is_paid = True
            order.save()
            return redirect('cchome')

        else:
            return redirect('cchome')
        
@method_decorator([csrf_exempt],name="dispatch")
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
    
@method_decorator([signin_required,never_cache],name='dispatch')
class MycourseView(View):
    def get(self,req):
        order_qs = Order.objects.filter(is_paid=True,student_object=req.user)
        return render(req,'mycourse.html',{'data':order_qs})

@method_decorator([signin_required,never_cache],name='dispatch')
class LessonView(View):
    def get(self,req,**kwargs):
        # print(kwargs.get('id'))
        # print(req.GET)
        course = Course.objects.get(id=kwargs.get('id'))
        module = Module.objects.filter(course = course).first()
        lesson = Lesson.objects.filter(module=module).first if  'lesson' not in req.GET else Lesson.objects.get(id=req.GET.get('lesson'))


        return render(req,'viewlessons.html',{'course':course,'lesson':lesson})
