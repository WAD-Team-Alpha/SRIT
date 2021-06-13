from django.shortcuts import render, redirect
from django.contrib import auth
from dashboard.models import *
from django.contrib.auth.models import User
from .models import *
from dashboard.models import *

# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        print(email)
        print(password)
        
        user = auth.authenticate(request, email=email, password=password)
        print(user)
        print(request.user)
        
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {"error": "wrong credentials"})
    
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        rollnumber = request.POST['rollnumber']
        password = request.POST['psw']

        if Student.objects.filter(email = email).exists():
            return redirect('signup')
        if Student.objects.filter(RollNumber = rollnumber).exists():
            return redirect('signup')
        
        user = User.objects.create_user(email=email, password=password)
        user.is_active = True
        user.save()

        return redirect('login')

    return render(request, 'signup.html')