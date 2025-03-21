from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError,transaction
from home.models import Patient
import logging


logger = logging.getLogger(__name__)

def registerUser(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if not (first_name and last_name and email and username and password and confirm_password):
            messages.error(request, "All fields are required!")
            return render(request, 'accounts/registeruser.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'accounts/registeruser.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'accounts/registeruser.html')

        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password  # set the password here
            )
            
            # Create the Customer instance if it doesn't exist
            if not hasattr(user, 'customer'):
                Patient.objects.create(user=user)

            messages.success(request, "Registration successful! Please log in.")
            return redirect("login-user")
        except IntegrityError as e:
            logger.error(f"IntegrityError during registration: {e}")
            messages.success(request, "Registration successful ! please log in.")
            return redirect('login-user')
        except Exception as e:
            logger.error(f"Unexpected error during registration: {e}")
            messages.error(request, "An unexpected error occurred. Please try again.")
            return render(request, 'accounts/registeruser.html')

    return render(request, 'accounts/registeruser.html')




def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            user= authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Incorrect Password!")
                return redirect('login-user')

        else:
            messages.error(request, "Username not found!")
            return redirect('login-user')

    return render(request, 'accounts/loginuser.html')

def logoutUser(request):
    logout(request)
    return redirect("login-user")