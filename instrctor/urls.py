from django.urls import path
from instrctor.views import InstructorSignupView
urlpatterns = [
    path('inssignup',InstructorSignupView.as_view(),name="inssignup")
]