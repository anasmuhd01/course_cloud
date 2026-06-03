from student.models import Cart,Wishlist

def cart_count(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(student_object  = request.user).count()
        wishlist_count = Wishlist.objects.filter(student_object = request.user).count()

        return {'cart_count':cart_count,'wishlist_count':wishlist_count}
    else:
        return {'cart_count':0,'wishlist_count':0}
    
    
