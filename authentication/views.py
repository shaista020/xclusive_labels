from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import pyotp
from django.contrib import messages
from decimal import Decimal

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

            # Set up 2FA if enabled
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
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  

            # Redirect based on user type
            if user.is_superuser:
                return redirect('/dashboard/')
            else:
                return redirect('/user_dashboard/')
        else:
            error = "Invalid username or password."

    return render(request, "signin.html", {"error": error})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('/auth/signin/')

def signup(request):
    referral_code = request.GET.get('referral_code')  # Get referral code from GET request

    print(f"Referral code received in GET request: {referral_code}")  # Debugging

    error_messages = []

    if request.method == 'POST':
        # Referral code from POST request (if any)
        referral_code = request.POST.get('referral_code', referral_code)
        print(f"Referral code received in POST request: {referral_code}")  # Debugging

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Validation
        if User.objects.filter(username=username).exists():
            error_messages.append("Username already exists.")

        if User.objects.filter(email=email).exists():
            error_messages.append("Email already exists.")

        if error_messages:
            return render(
                request,
                "signup.html",
                {
                    "error": " ".join(error_messages),
                    "referral_code": referral_code,
                },
            )

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        print(f"Created user: {user.username}")

        # Generate referral code
        user.generate_referral_code()
        user.save()
        print(f"Generated referral code for user: {user.referral_code}")

        if referral_code:
            print(f"Handling referral code: {referral_code}")  # Debugging
            referrer = User.objects.filter(referral_code=referral_code).first()
            if referrer:
                print(f"Referrer: {referrer}")  # Debugging
                user.referred_by = referrer
                user.save()

                # Add 10% commission
                from decimal import Decimal
                referrer.available_for_withdraw += Decimal('100.00')  # Use Decimal for compatibility
                referrer.save()
                print(f"Updated referrer's available_for_withdraw: {referrer.available_for_withdraw}")
            else:
                print(f"No valid referrer found for referral code: {referral_code}")
        else:
            print("No referral code provided")

        # Send welcome email
        send_mail(
            'Welcome to Our Website!',
            'Thank you for signing up with us. We are excited to have you on board!',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        print("Email sent successfully.")

        return redirect('/auth/signin/')

    # Build referral link
    referral_link = request.build_absolute_uri(f"/auth/signup/?referral_code={request.user.referral_code}") if request.user.is_authenticated else None

    return render(request, "signup.html", {"referral_code": referral_code, "referral_link": referral_link})


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

# Resend OTP for 2FA
def resend_otp(request):
    if request.user.is_authenticated and request.user.is_2fa_enabled:
        user = request.user
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

        messages.success(request, "A new OTP has been sent to your email.")
    return redirect('/auth/verify-2fa/')
