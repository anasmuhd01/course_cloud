from django.urls import path
from student.views import *

urlpatterns = [
    path('signup',SignupView.as_view(),name='signup'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('cchome',CCHomeView.as_view(),name='cchome'),
    path('coursedetails/<int:cid>',CourseDetailsView.as_view(),name='course_details'),
    path('cart/<int:id>',AddtoCart.as_view(),name="addtocart"),
    path('cartlist',CartlistView.as_view(),name="cartlist"),
    path('deleteitem/<int:id>',DeleteCartItemView.as_view(),name="dltcartitm")
]