from authpage.models import Student
from .models import *
from django.core.files.storage import FileSystemStorage
import numpy as np
from matplotlib import pyplot as plt
from django.shortcuts import render
import random
import matplotlib
matplotlib.use('Agg')
from authpage.cse import *
from authpage.ece import *
from authpage.mech import *
from authpage.eee import *
from authpage.civil import *
from authpage.views import createSemester, createMarks
# Create your views here.


def dashboard(request):
    if request.method == 'POST':
        sti = request.POST['sti']
        oti = request.POST['oti']
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        rollnum = student.roll_no
        sem_no = student.sem_no

        Semester.objects.all().filter(roll_no=rollnum, sem_no=sem_no).update(cst=sti, ot=oti)
        details = Semester.objects.all().filter(roll_no=rollnum, sem_no=sem_no).get()
        context = {
            'sti': details.cst,
            'oti': details.ot,
            'stp': details.csp,
            'otp': details.op
        }

        return render(request, 'dashboard.html', context)
    else:
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        rollnum = student.roll_no
        sem_no = student.sem_no
        details = Semester.objects.all().filter(roll_no=rollnum, sem_no=sem_no).get()
        context = {
            'sti': details.cst,
            'oti': details.ot,
            'stp': details.cst,
            'otp': details.ot
        }

        return render(request, 'dashboard.html', context)

def calculateInternal(mid1, mid2):
    internal = []
    m1 = [int(mid1.s1),int(mid1.s2),int(mid1.s3),int(mid1.s4),int(mid1.s5),int(mid1.s6),int(mid1.s7),int(mid1.s8)]
    m2 = [int(mid2.s1),int(mid2.s2),int(mid2.s3),int(mid2.s4),int(mid2.s5),int(mid2.s6),int(mid2.s7),int(mid2.s8)]

    m = zip(m1, m2)

    for i,j in m:
        if i > j:
            x = i*0.8 + j*0.2
        else:
            x = i*0.2 + j*0.8
        internal.append(x)
    return internal

def predictExternal(internal):
    external = []
    for i in internal:
        external.append(1.5*i + 28)

    return external

def calculateCsp(marks):
    internal = [int(marks['is1']),int(marks['is1']),int(marks['is1']),int(marks['is1']),int(marks['is1']),int(marks['is1']),int(marks['is1']),int(marks['is1'])]
    external = [int(marks['es1']),int(marks['es1']),int(marks['es1']),int(marks['es1']),int(marks['es1']),int(marks['es1']),int(marks['es1']),int(marks['es1'])]

    total = zip(internal, external)
    c = 0
    for i, j in total:
        c = c+i+j
    
    c = c/8

    return c


def marks(request):
    if request.method == "POST":
        marks = request.POST
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        rollnum = student.roll_no
        sem_no = student.sem_no

        for i in range(2):
            Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=i).update(
                s1 = marks['m{j}s1'.format(j=i)],
                s2 = marks['m{j}s2'.format(j=i)],
                s3 = marks['m{j}s3'.format(j=i)],
                s4 = marks['m{j}s4'.format(j=i)],
                s5 = marks['m{j}s5'.format(j=i)],
                s6 = marks['m{j}s6'.format(j=i)],
                s7 = marks['m{j}s7'.format(j=i)],
                s8 = marks['m{j}s8'.format(j=i)]
            )

        mid1 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=0).get()
        mid2 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=1).get()

        internal = calculateInternal(mid1, mid2)

        createMarks(sem_no, rollnum, 2, internal[0],internal[1],internal[2],internal[3],internal[4],internal[5],internal[6],internal[7])

        external = predictExternal(internal)

        createMarks(sem_no, rollnum, 3, external[0],external[1],external[2],external[3],external[4],external[5],external[6],external[7])

        mid1 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=0).get()
        mid2 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=1).get()
        ext = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=3).get()
        
        return render(request, 'marks.html',{'m1': mid1, 'm2': mid2, 'e': ext})
    else:
        student = Student.objects.all().filter(Username=request.user.username).get()
        rollnum = student.RollNumber
        sem_no = student.sem_no
        mid1 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=0).get()
        mid2 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=1).get()
        ext = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=3).get()
        
        return render(request, 'marks.html',{'m1': mid1, 'm2': mid2, 'e': ext})

def previousmarks(request):
    if request.method == 'POST':
        student = Student.objects.all().filter(Username=request.user.username).get()
        rollnum = student.RollNumber
        branch = student.branch
        marks = request.POST
        createMarks(marks['sem_no'], rollnum, 2, marks['is1'],marks['is2'],marks['is3'],marks['is4'],marks['is5'],marks['is6'],marks['is7'],marks['is8'])
        createMarks(marks['sem_no'], rollnum, 3, marks['es1'],marks['es2'],marks['es3'],marks['es4'],marks['es5'],marks['es6'],marks['es7'],marks['es8'])

        cur_per = calculateCsp(marks)

        if branch == 'CSE':
            createSemester(cse, marks['sem_no'], rollnum, 1, cur_per)
        elif branch == 'ECE':
            createSemester(ece, marks['sem_no'], rollnum, 1, cur_per)
        elif branch == 'MECH':
            createSemester(mech, marks['sem_no'], rollnum, 1, cur_per)
        elif branch == 'CIVIL':
            createSemester(civil, marks['sem_no'], rollnum, 1, cur_per)
        else:
            createSemester(eee, marks['sem_no'], rollnum, 1, cur_per)

        return render(request, 'previous.html')
        
    return render(request, 'previous_matrks.html')


def activities(request):
    return render(request, 'activities.html')


def subjectWise(request):
    return render(request, 'subjectWise.html')


def overall(request):
    return render(request, 'overall.html')


def report(request):
    return render(request, 'report.html')


def suggestion(request):
    return render(request, 'suggestion.html')