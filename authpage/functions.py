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

def createSemester(lis, sem_no, rollnumber, status, cp=0, ot=0):
    Semester.objects.create(
        sem_no=sem_no,
        roll_no=rollnumber,
        status=status,
        cst=0,
        ot=ot,
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

def createSemester8(lis, sem_no, rollnumber, status, cp=0, ot=0):
    Semester.objects.create(
        sem_no=sem_no,
        roll_no=rollnumber,
        status=status,
        cst=0,
        ot=ot,
        csp=cp,
        op=0,
        s1=lis[int(sem_no)][0],
        s2=lis[int(sem_no)][1],
    )


def createMarks(sem_no, rollnumber, type, s1=0, s2=0, s3=0, s4=0, s5=0, s6=0, s7=0, s8=0):
    Marks.objects.create(
        sem_no=sem_no,
        roll_no=rollnumber,
        type=type,
        s1=s1,
        s2=s2,
        s3=s3,
        s4=s4,
        s5=s5,
        s6=s6,
        s7=s7,
        s8=s8,
    )


def createMarks8(sem_no, rollnumber, type, s1=0, s2=0, s3=0, s4=0, s5=0, s6=0, s7=0, s8=0):
    Marks.objects.create(
        sem_no=sem_no,
        roll_no=rollnumber,
        type=type,
        s1=s1,
        s2=s2,
    )


def updateMarks(sem_no, rollnumber, type, s1=0, s2=0, s3=0, s4=0, s5=0, s6=0, s7=0, s8=0):
    Marks.objects.all().filter(sem_no=int(sem_no), roll_no=rollnumber, type=type).update(
        s1=int(s1),
        s2=int(s2),
        s3=int(s3),
        s4=int(s4),
        s5=int(s5),
        s6=int(s6),
        s7=int(s7),
        s8=int(s8),
    )


def updateMarks8(sem_no, rollnumber, type, s1=0, s2=0, s3=0, s4=0, s5=0, s6=0, s7=0, s8=0):
    Marks.objects.all().filter(sem_no=int(sem_no), roll_no=rollnumber, type=type).update(
        s1=int(s1),
        s2=int(s2),
    )

def updateSemester(lis, sem_no, rollnumber, status, cp, ot):
    Semester.objects.all().filter(sem_no=int(sem_no), roll_no=rollnumber).update(
        sem_no=int(sem_no),
        roll_no=rollnumber,
        status=status,
        cst=0,
        ot=ot,
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

def updateSemester8(lis, sem_no, rollnumber, status, cp, ot):
    Semester.objects.all().filter(sem_no=sem_no, roll_no=rollnumber).update(
        sem_no=sem_no,
        roll_no=rollnumber,
        status=status,
        cst=0,
        ot=ot,
        csp=cp,
        op=0,
        s1=lis[int(sem_no)][0],
        s2=lis[int(sem_no)][1],
    )