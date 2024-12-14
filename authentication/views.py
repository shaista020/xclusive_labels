from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your views here.
User = get_user_model()
# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username , password = password)
        print(user)
        if user is not None:
            login(request, user)
            is_superuser = user.is_superuser
            if is_superuser is True:
                return redirect('/dashboard/')
            else:
                return redirect("/user_dashboard/")
        else:
            error = "Invalid Credentials"
            return render(request, "signin.html", {"error": error})
    return render(request, "signin.html")


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            error_username = "Username already exists"
            return render(request, "signup.html", {"error_username": error_username})

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            error_email = "Email already exists"
            return render(request, "signup.html", {"error_email": error_email})

        # Create the new user
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return redirect('/auth/signin/')

    return render(request, "signup.html")

def user_logout(request):
    logout(request)
    return redirect('/')
        