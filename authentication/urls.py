from django.urls import path
from . import views 
urlpatterns = [
    path('signin/', views.user_login, name='signin'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),  
]
