from django.urls import path
from . import views

urlpatterns = [
    path('',views.signup,name='signup'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('pincode/',views.pincode,name='pincode'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('homepage/', views.homepage, name='homepage'),
    path('login/', views.user_login, name='login'),
    path('user_logout/',views.user_logout, name='logout'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('forgot_pswd_verify/', views.verify_forgot_password_otp, name='forgot_pswd_verify'),
    path('forgot_pswd_reset/', views.forgot_pswd_reset, name='forgot_pswd_reset'),
    path('set_pincode/', views.set_pincode, name='set_pincode'),
    path('set_city/', views.set_city, name='set_city'),
]