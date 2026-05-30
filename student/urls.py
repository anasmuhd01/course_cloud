from django.urls import path
from student.views import *

urlpatterns = [
    path('signup',SignupView.as_view(),name='signup')
]