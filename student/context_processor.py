from student.models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(student_object  = request.user).count()
        return {'cart_count':count}
    else:
        return {'cart_count':0}