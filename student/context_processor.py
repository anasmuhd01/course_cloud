from student.models import Cart,Wishlist,Order

def cart_count(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(student_object  = request.user).count()
        wishlist_count = Wishlist.objects.filter(student_object = request.user).count()
        qs=Order.objects.filter(is_paid=True,student_object=request.user)
        course_count=0
        for i in qs:
            course_count+=i.course_object.count()

        return {'cart_count':cart_count,'wishlist_count':wishlist_count,'total_order':course_count}
    else:
        return {'cart_count':0,'wishlist_count':0,'total_order':0}
    
    
