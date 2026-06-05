from django.urls import path
from student.views import *

urlpatterns = [
    path('signup',SignupView.as_view(),name='signup'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('cchome',CCHomeView.as_view(),name='cchome'),
    path('coursedetails/<int:cid>',CourseDetailsView.as_view(),name='course_details'),
    path('cart/<int:id>',AddtoCart.as_view(),name="addtocart"),
    path('cartlist',CartlistView.as_view(),name="cartlist"),
    path('deleteitem/<int:id>',DeleteCartItemView.as_view(),name="dltcartitm"),
    path('wishlist/<int:id>',WishlistView.as_view(),name="wishlist"),
    path('wishlistall',WishlistAllView.as_view(),name='wishlistall'),
    path('dltwlst/<int:id>',DeleteWishlistView.as_view(),name="dltwlst"),
    path('payment',PlaceOrderView.as_view(),name='placeorder'),
    path('paymentverify',Paymentview.as_view(),name='paysuccess'),
    path('mycourse',MycourseView.as_view(),name='mycourse'),
    path('viewlesson/<int:id>',LessonView.as_view(),name='viewlesson')
]