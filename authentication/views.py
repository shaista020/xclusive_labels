from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import pyotp
import qrcode
from io import BytesIO
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import pyotp
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()
def user_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST.get('remember') 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if user.is_2fa_enabled and not user.otp_secret:
                user.otp_secret = pyotp.random_base32()  
                user.save()
            if user.is_2fa_enabled:
                totp = pyotp.TOTP(user.otp_secret)
                otp = totp.now()
                request.session['otp'] = otp
                send_mail(
                    'Your OTP for 2FA Verification',
                    f'Your OTP is {otp}. It is valid for the next 30 seconds.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                request.session['is_2fa_verified'] = False  
                return redirect('/auth/verify-2fa/')  
            if remember:
                request.session.set_expiry(1209600)  
            else:
                request.session.set_expiry(0)  
            if user.is_superuser:
                return redirect('/dashboard/')
            else:
                return redirect('/user_dashboard/')
        else:
            error = "Invalid Credentials"

    return render(request, "signin.html", {"error": error})


# Logout view
def user_logout(request):
    logout(request)
    return redirect('/auth/signin/')



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error_username": "Username already exists"})
        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {"error_email": "Email already exists"})
        user = User.objects.create_user(username=username, email=email, password=password)
        send_mail(
            'Welcome to Our Website!',
            'Thank you for signing up with us. We are excited to have you on board!',
            settings.EMAIL_HOST_USER,  
            [email], 
            fail_silently=False,  
        )

        return redirect('/auth/signin/')

    return render(request, "signup.html")


def verify_2fa(request):
    error = None
    if request.method == "POST":
        otp = request.POST['otp']
        session_otp = request.session.get('otp')

        if otp == session_otp:
            request.session['is_2fa_verified'] = True  
            if request.user.is_superuser:
                return redirect('/dashboard/')
            else:
                return redirect('/user_dashboard/')
        else:
            error = "Invalid OTP. Please try again or request a new one."

    return render(request, "verify_2fa.html", {"error": error})


def resend_otp(request):
    if request.user.is_authenticated and request.user.is_2fa_enabled:
        user = request.user
        totp = pyotp.TOTP(user.otp_secret)
        otp = totp.now()
        print(f"Generated OTP: {otp}")
        request.session['otp'] = otp

        send_mail(
            'Your OTP for 2FA Verification',
            f'Your OTP is {otp}. It is valid for the next 30 seconds.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        print(f"OTP stored in session: {request.session.get('otp')}")

        messages.success(request, "A new OTP has been sent to your email.")
    return redirect('/auth/verify-2fa/')
