from django.urls import path
from student.views import *

urlpatterns = [
    path('signup',SignupView.as_view(),name='signup'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('cchome',CCHomeView.as_view(),name='cchome'),
]