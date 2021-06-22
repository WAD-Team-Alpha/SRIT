from django.shortcuts import render, redirect
from django.contrib import auth
from dashboard.models import *
from django.contrib.auth.models import User
from .models import *
from dashboard.models import *
from .cse import *
from .civil import *
from .ece import *
from .eee import *
from .mech import *
from .forms import *
from django.contrib import messages
from .functions import *
from django.contrib.auth.hashers import make_password

# Create your views here.

student = None


def login(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pass']

        print(username)
        print(password)

        user = auth.authenticate(request, username=username, password=password)
        print(user)
        print(request.user)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Logged in")
            return redirect('home')
        else:
            messages.error(request, 'Wrong credentials')
            return redirect('login')
    
    print(request.user)
    return render(request, 'signin.html')


def logout(request):
    auth.logout(request)
    messages.success(request, "Logged out")
    return redirect('login')

def securityCheck(request): 
    global student
    if request.method == 'POST':
        usr_nm = request.POST['uname']
        scode = request.POST['scode']
        student = Student.objects.all().filter(usr_nm=usr_nm).get()
        if (str(scode) == str(student.security_code)):
            messages.success(request, "Security code accessed")
            return redirect('forgot_password')
        else:
            return render(request, 'security_code.html', {"error": "Invalid Security Code"})
    return render(request, 'security_code.html')

def forgotPassword(request): 
    if request.method == 'POST': 
        password = request.POST['npsw']
        user = User.objects.all().filter(username=student.usr_nm).get()
        user.password = make_password(password)
        user.save()
        messages.success(request, 'Password changed sucessfully')
        return redirect('login')
    return render(request, 'forgot_password.html')

def signup(request):
    if request.method == 'POST':
        userform = StudentForm(request.POST)

        email = request.POST['email']
        username = request.POST['usr_nm']
        rollnumber = request.POST['roll_no']
        roll_no = rollnumber
        print(roll_no)
        password = request.POST['pass']
        branch = request.POST['branch']
        sem_no = request.POST['sem_no']

        if userform.is_valid():
            if Student.objects.filter(email=email).exists():
                return redirect('signup')
            if Student.objects.filter(roll_no=rollnumber).exists():
                return redirect('signup')

            print(roll_no)

            if sem_no == '8':
                print("i am here")
                if branch == 'CSE':
                    createSemester8(cse, 8, rollnumber, 0)
                elif branch == 'ECE':
                    createSemester8(ece, 8, rollnumber, 0)
                elif branch == 'MECH':
                    createSemester8(mech, 8, rollnumber, 0)
                elif branch == 'CIVIL':
                    createSemester8(civil, 8, rollnumber, 0)
                else:
                    createSemester8(eee, 8, rollnumber, 0)

                createMarks8(sem_no, rollnumber, 0)
                createMarks8(sem_no, rollnumber, 1)
                createMarks8(sem_no, rollnumber, 2)
                createMarks8(sem_no, rollnumber, 3)
                createMarks8(sem_no, rollnumber, 4)

            else:
                print("i am not here")
                if branch == 'CSE':
                    createSemester(cse, sem_no, roll_no, 0)
                elif branch == 'ECE':
                    createSemester(ece, sem_no, rollnumber, 0)
                elif branch == 'MECH':
                    createSemester(mech, sem_no, rollnumber, 0)
                elif branch == 'CIVIL':
                    createSemester(civil, sem_no, rollnumber, 0)
                else:
                    createSemester(eee, sem_no, rollnumber, 0)

                createMarks(sem_no, rollnumber, 0)
                createMarks(sem_no, rollnumber, 1)
                createMarks(sem_no, rollnumber, 2)
                createMarks(sem_no, rollnumber, 3)
                createMarks(sem_no, rollnumber, 4)

            user = User.objects.create_user(
                email=email, password=password, username=username)
            user.is_active = True
            userform.save()
            user.save()
        else:
            messages.error(request, "Please enter valid info")
            return render(request, 'signup.html', {'form': userform})

        messages.success(request, "Registered Successfully, you can now login")
        return redirect('login')
    else:
        userform = StudentForm()
        return render(request, 'signup.html', {'form': userform})
