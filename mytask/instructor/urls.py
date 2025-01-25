from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.register_instructor, name='register_instructor'),
    path('login/',views.login_instructor, name='login_instructor'),
    path('verify-email-otp/',views.verify_email_otp, name='verify_email_otp'),
]