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

def createSemester(lis, sem_no, rollnumber, status, cp=0):
    Semester.objects.create(
        sem_no=sem_no,
        roll_no=rollnumber,
        status=status,
        cst=0,
        ot=0,
        csp=cp,
        op=0,
        s1=lis[int(sem_no)][0],
        s2=lis[int(sem_no)][1],
        s3=lis[int(sem_no)][2],
        s4=lis[int(sem_no)][3],
        s5=lis[int(sem_no)][4],
        s6=lis[int(sem_no)][5],
        s7=lis[int(sem_no)][6],
        s8=lis[int(sem_no)][7],
    )

def createMarks(sem_no, rollnumber, type, s1=0, s2=0, s3=0, s4=0, s5=0, s6=0, s7=0, s8=0):
    Marks.objects.create(
        sem_no=sem_no, 
        roll_no=rollnumber, 
        type= type, 
        s1 = s1,
        s2 = s2,
        s3 = s3,
        s4 = s4,
        s5 = s5,
        s6 = s6,
        s7 = s7,
        s8 = s8,
    )


def signup(request):
    if request.method == 'POST':
        userform = StudentForm(request.POST)

        email = request.POST['email']
        username = request.POST['usr_nm']
        rollnumber = request.POST['rollnumber']
        password = request.POST['psw']
        branch = request.POST['branch']
        sem_no = request.POST['sem_no']
        
        if userform.is_valid():
            if Student.objects.filter(email = email).exists():
                return redirect('signup')
            if Student.objects.filter(RollNumber = rollnumber).exists():
                return redirect('signup')

            user = User.objects.create_user(email=email, password=password, username=username)
            user.is_active = True
            user.save()

            if branch == 'CSE':
                createSemester(cse, sem_no, rollnumber, 0)
            elif branch == 'ECE':
                createSemester(ece, sem_no, rollnumber, 0)
            elif branch == 'MECH':
                createSemester(mech, sem_no, rollnumber, 0)
            elif branch == 'CIVIL':
                createSemester(civil, sem_no, rollnumber, 0)
            else:
                createSemester(eee, sem_no, rollnumber, 0)

            userform.save()
            createMarks(sem_no, rollnumber, 0)
            createMarks(sem_no, rollnumber, 1)
            createMarks(sem_no, rollnumber, 2)
            createMarks(sem_no, rollnumber, 3)
            createMarks(sem_no, rollnumber, 4)
        else:
            return render(request, 'isignup.html', {'form': userform})

        return redirect('login')
    else:
        userform = StudentForm()
        return render(request, 'signup.html', {'form': userform})
