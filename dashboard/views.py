from authpage.models import Student
from .models import *
from django.core.files.storage import FileSystemStorage
import numpy as np
from matplotlib import pyplot as plt
from django.shortcuts import render
# import random
import matplotlib
matplotlib.use('Agg')
from authpage.cse import *
from authpage.ece import *
from authpage.mech import *
from authpage.eee import *
from authpage.civil import *
from authpage.views import createSemester, createMarks, updateMarks
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

        return render(request, 'index.html', context)
    else:
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        rollnum = student.roll_no
        sem_no = student.sem_no
        details = Semester.objects.all().filter(roll_no=rollnum, sem_no=sem_no).get()
        context = {
            'sti': details.cst,
            'oti': details.ot,
            'stp': details.csp,
            'otp': details.op
        }

        return render(request, 'index.html', context)

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
        external.append(1.406*i + 25.625)

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
                s1 = marks['s1m{j}'.format(j=i+1)],
                s2 = marks['s2m{j}'.format(j=i+1)],
                s3 = marks['s3m{j}'.format(j=i+1)],
                s4 = marks['s4m{j}'.format(j=i+1)],
                s5 = marks['s5m{j}'.format(j=i+1)],
                s6 = marks['s6m{j}'.format(j=i+1)],
                s7 = marks['s7m{j}'.format(j=i+1)],
                s8 = marks['s8m{j}'.format(j=i+1)]
            )

        mid1 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=0).get()
        mid2 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=1).get()

        internal = calculateInternal(mid1, mid2)

        updateMarks(sem_no, rollnum, 2, internal[0],internal[1],internal[2],internal[3],internal[4],internal[5],internal[6],internal[7])

        external = predictExternal(internal)

        updateMarks(sem_no, rollnum, 3, external[0],external[1],external[2],external[3],external[4],external[5],external[6],external[7])

        mid1 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=0).get()
        mid2 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=1).get()
        ext = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=3).get()
        sub = Semester.objects.all().filter(sem_no=sem_no, roll_no=rollnum, status=0).get()
        
        return render(request, 'current_marks.html',{'m1': mid1, 'm2': mid2, 'e': ext, 's': sub})
    else:
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        rollnum = student.roll_no
        sem_no = student.sem_no
        mid1 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=0).get()
        mid2 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=1).get()
        ext = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=3).get()
        sub = Semester.objects.all().filter(sem_no=sem_no, roll_no=rollnum, status=0).get()
        
        return render(request, 'current_marks.html',{'m1': mid1, 'm2': mid2, 'e': ext, 's': sub})

def prevSems():
    return []

def previousmarks(request):
    if request.method == 'POST':
        student = Student.objects.all().filter(Username=request.user.username).get()
        rollnum = student.RollNumber
        branch = student.branch
        marks = request.POST
        updateMarks(marks['sem_no'], rollnum, 2, marks['is1'],marks['is2'],marks['is3'],marks['is4'],marks['is5'],marks['is6'],marks['is7'],marks['is8'])
        updateMarks(marks['sem_no'], rollnum, 3, marks['es1'],marks['es2'],marks['es3'],marks['es4'],marks['es5'],marks['es6'],marks['es7'],marks['es8'])

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

        return render(request, 'previous_marks.html')
    else:
        semList = prevSems() 
        return render(request, 'previous_marks.html')


def activities(request):
    student = Student.objects.all().filter(Username=request.user.username).get()

    rollnum = student.roll_no
    semNum = Student.sem_no
    subjectName = Semester.objects.all().filter(
        roll_no=rollnum, sem_no=semNum,).get()
    context = {
        'student': student,
        'names': subjectName,
    }
    return render(request, 'activities.html', context)


def savePieChart(m1, m2, quiz, extra_curricular, imgName, subjectName):
    labels = 'mid-1', 'mid-2', 'quiz', 'other activities'
    sizes = [m1, m2,  quiz, extra_curricular]
    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = (0.1, 0.1, 0.1, 0.1)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')
    plt.title("Pie chart of "+subjectName+"")
    plt.savefig('media/'+imgName+'.png', dpi=100)
    plt.close()


def subjectWise(request):

    student = Student.objects.all().filter(Username=request.user.username).get()

    rollnum = student.roll_no
    semNum = Student.sem_no
    subjectName = Semester.objects.all().filter(
        roll_no=rollnum, sem_no=semNum,).get()

    m1 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=0).get()
    m2 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=1).get()
    quiz = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).get()
    extra_curricular = Marks.objects.all().filter(
        roll_no=rollnum, sem_no=semNum, type=5).get()
    savePieChart(m1.s1, m2.s1, quiz.s1, extra_curricular.s1,
                 'image1', subjectName.s1)
    savePieChart(m1.s2, m2.s2, quiz.s2, extra_curricular.s2,
                 'image2', subjectName.s2)
    if semNum != 8:
        savePieChart(m1.s3, m2.s3, quiz.s3,
                     extra_curricular.s3, 'image3', subjectName.s3)
        savePieChart(m1.s4, m2.s4, quiz.s4,
                     extra_curricular.s4, 'image4', subjectName.s4)
        savePieChart(m1.s5, m2.s5, quiz.s5,
                     extra_curricular.s5, 'image5', subjectName.s5)
        savePieChart(m1.s6, m2.s6, quiz.s6,
                     extra_curricular.s6, 'image6', subjectName.s6)
        savePieChart(m1.s7, m2.s7, quiz.s7,
                     extra_curricular.s7, 'image7', subjectName.s7)
        savePieChart(m1.s8, m2.s8, quiz.s8,
                     extra_curricular.s8, 'image8', subjectName.s8)
    else:
        pass

    return render(request, 'subjectWise.html')


def overall(request):
    student = Student.objects.all().filter(
        Username=request.user.username).get()
    rollnum = student.roll_no
    semNum = Student.sem_no
    subjectName = Semester.objects.all().filter(
        roll_no=rollnum, sem_no=semNum,).get()
    m1 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=0).get()
    m2 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=1).get()
    quiz = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).get()
    extra_curricular = Marks.objects.all().filter(
        roll_no=rollnum, sem_no=semNum, type=5).get()
    subject1 = (m1.S1 + m2.S1)*100/60
    subject2 = (m1.S2 + m2.S2)*100/60
    if semNum != 8:
        subject3 = (m1.S3 + m2.S3)*100/60
        subject5 = (m1.S5 + m2.S5)*100/60
        subject4 = (m1.S4 + m2.S4)*100/60
        subject6 = (m1.S6 + m2.S6)*100/60
        subject7 = (m1.S7 + m2.S7)*100/60
        subject8 = (m1.S8 + m2.S8)*100/60
    else:
        pass

    if semNum != 8:
        marks = [subject1, subject2, subject3, subject4,
                 subject5, subject6, subject7, subject8]
        subjectNames = [subjectName.s1, subjectName.s2, subjectName.s2,
                        subjectName.s4, subjectName.s5, subjectName.s6, subjectName.s7, subjectName.s8, ]
    else:
        marks = [subject1, subject2]
        subjectNames = [subjectName.s1, subjectName.s2]

    # data = {'subject1': subject1, 'subject2': subject2,
    #         'subject3': subject3, 'subject4': subject4, 'subject5': subject5, 'subject6': subject6, }

    courses = subjectNames
    values = marks

    fig = plt.figure(figsize=(10, 5))
    my_colors = ['red', 'blue', 'green', 'cyan', 'Purple', 'pink']
    # creating the bar plot
    plt.bar(courses, values, color=my_colors,
            width=0.4)

    plt.xlabel("Subjects")
    plt.ylabel("Score in Each Subject")
    plt.title("Overall Trends")
    plt.savefig('media/overall_barchart.png', dpi=100)
    plt.close()
    return render(request, 'overall.html')


def report(request):
    student = Student.objects.all().filter(usr_nm=request.user.username).get()
    rollnum = student.roll_no
    semNum = student.sem_no
    subjectName = Semester.objects.all().filter(roll_no=rollnum, sem_no=semNum,).get()
   
    if semNum == 8:
        m1 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=0).get()
        m2 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=1).get()
        sub1 = m1.s1+m2.s1
        sub2 = m1.s2+m2.s2
        marks1 = [sub1,sub2]
        marks1.sort(reverse = True)
        # print(marks1)
        l_s2 = marks1[0]
        l_s1 = marks1[1]
        if sub1==l_s1:
            least_subject1 = subjectName.s1
        if sub2==l_s1:
            least_subject1 = subjectName.s2
        
        if sub1==l_s2:
            least_subject2 = subjectName.s1
        if sub2==l_s2:
            least_subject2 = subjectName.s2

        subjects_focused = [least_subject1,least_subject2]
        context = {
            'Subjects_focused' : subjects_focused
        }
        return render(request, 'report.html',context)

    else:
        m1 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=0).get()
        m2 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=1).get()
        Subjects_names = [subjectName.s1,subjectName.s2,subjectName.s3,subjectName.s4,subjectName.s5,subjectName.s6,subjectName.s7,subjectName.s8]
        
        sub1 = m1.s1+m2.s1
        sub2 = m1.s2+m2.s2
        sub3 = m1.s3+m2.s3
        sub4 = m1.s4+m2.s4
        sub5 = m1.s5+m2.s5
        sub6 = m1.s6+m2.s6
        sub7 = m1.s7+m2.s7
        sub8 = m1.s8+m2.s8

        sub = [sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8]

        # diff1 = m1.s1-m2.s1
        # diff2 = m1.s2-m2.s2
        # diff3 = m1.s3-m2.s3
        # diff4 = m1.s4-m2.s4
        # diff5 = m1.s5-m2.s5
        # diff6 = m1.s6-m2.s6
        # diff7 = m1.s7-m2.s7
        # diff8 = m1.s8-m2.s8

        mid1 = [m1.s1,m1.s2,m1.s3,m1.s4,m1.s5,m1.s6,m1.s7,m1.s8]
        mid2 = [m2.s1,m2.s2,m2.s3,m2.s4,m2.s5,m2.s6,m2.s7,m2.s8]

        # diff = [diff1,diff2,diff3,diff4,diff5,diff6,diff7,diff8]

        subjects_weak = []
        for num in range(8):
            if mid1[num]>mid2[num]:
                subjects_weak.append(mid1[num])

        # print(subjects_weak)

        subjects_strong = []
        for num in range(8):
            if mid1[num]<mid2[num]:
                subjects_strong.append(mid2[num])

        # print(subjects_strong)

       
            

            
        marks1 = [sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8]
        marks1.sort(reverse = True)
        print(marks1)
        l_s3 = marks1[5]
        l_s2 = marks1[6]
        l_s1 = marks1[7]


         
        # for i in list(range(8)):
        #     if sub[i] == l_s3:
        #         least_subject3 = Subjects_names[i]
        #         sub = sub.remove(sub[i])
        # print(least_subject3)

        if sub1==l_s1:
            least_subject1 = subjectName.s1
        elif sub2==l_s1 :
            least_subject1 = subjectName.s2
        elif sub3==l_s1:
            least_subject1 = subjectName.s3
        elif sub4==l_s1:
            least_subject1 = subjectName.s4
        elif sub5==l_s1:
            least_subject1 = subjectName.s5
        elif sub6==l_s1:
            least_subject1 = subjectName.s6
        elif sub7==l_s1:
            least_subject1 = subjectName.s7
        else:
            least_subject1 = subjectName.s8
        # print(least_subject1)

        if sub1==l_s2 & sub1!=l_s1:
            least_subject2 = subjectName.s1
        elif sub2==l_s2:
            least_subject2 = subjectName.s2
        elif sub3==l_s2:
            least_subject2 = subjectName.s3
        elif sub4==l_s2:
            least_subject2 = subjectName.s4
        elif sub5==l_s2:
            least_subject2 = subjectName.s5
        elif sub6==l_s2:
            least_subject2 = subjectName.s6
        elif sub7==l_s2:
            least_subject2 = subjectName.s7
        else:
            least_subject2 = subjectName.s8
        # print(least_subject2)

        if sub1==l_s3 & sub1!=l_s2 & sub1!=l_s1:
            least_subject3 = subjectName.s1
        elif sub2==l_s3:
            least_subject3 = subjectName.s2
        elif sub3==l_s3:
            least_subject3 = subjectName.s3
        elif sub4==l_s3:
            least_subject3 = subjectName.s4
        elif sub5==l_s3:
            least_subject3 = subjectName.s5
        elif sub6==l_s3:
            least_subject3 = subjectName.s6
        elif sub7==l_s3:
            least_subject3 = subjectName.s7
        else:
            least_subject3 = subjectName.s8
        
        

        subjects_focused = [least_subject1,least_subject2,least_subject3]
        
        subjects_good = list(set(Subjects_names) - set(subjects_focused)) 
        context={
            'Subjects_focused' : subjects_focused,
            'Subjects_good' : subjects_good,
            'Subjects_strong':subjects_strong
        }

        return render(request, 'report.html',context)


def suggestion(request):
    student = Student.objects.all().filter(usr_nm=request.user.username).get()
    rollnum = student.roll_no
    semNum = student.sem_no
    subjectName = Semester.objects.all().filter(roll_no=rollnum, sem_no=semNum,).get()
   
    if semNum == 8:
        m1 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=0).get()
        m2 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=1).get()
        sub1 = m1.s1+m2.s1
        sub2 = m1.s2+m2.s2
        marks1 = [sub1,sub2]
        marks1.sort(reverse = True)
        print(marks1)
        l_s2 = marks1[0]
        l_s1 = marks1[1]
        if sub1==l_s1:
            least_subject1 = subjectName.s1
        if sub2==l_s1:
            least_subject1 = subjectName.s2
        
        if sub1==l_s2:
            least_subject2 = subjectName.s1
        if sub2==l_s2:
            least_subject2 = subjectName.s2

        subjects = [least_subject1,least_subject2]
        context = {
            'Subjects' : subjects
        }
        return render(request, 'suggestions.html',context)

    else:
        m1 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=0).get()
        m2 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=1).get()
        sub1 = m1.s1+m2.s1
        sub2 = m1.s2+m2.s2
        sub3 = m1.s3+m2.s3
        sub4 = m1.s4+m2.s4
        sub5 = m1.s5+m2.s5
        sub6 = m1.s6+m2.s6
        sub7 = m1.s7+m2.s7
        sub8 = m1.s8+m2.s8
        marks1 = [sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8]
        marks1.sort(reverse = True)
        print(marks1)
        l_s3 = marks1[5]
        l_s2 = marks1[6]
        l_s1 = marks1[7]

        if sub1==l_s1:
            least_subject1 = subjectName.s1
        if sub2==l_s1:
            least_subject1 = subjectName.s2
        if sub3==l_s1:
            least_subject1 = subjectName.s3
        if sub4==l_s1:
            least_subject1 = subjectName.s4
        if sub5==l_s1:
            least_subject1 = subjectName.s5
        if sub6==l_s1:
            least_subject1 = subjectName.s6
        if sub7==l_s1:
            least_subject1 = subjectName.s7
        if sub8==l_s1:
            least_subject1 = subjectName.s8
        print(least_subject1)

        if sub1==l_s2:
            least_subject2 = subjectName.s1
        if sub2==l_s2:
            least_subject2 = subjectName.s2
        if sub3==l_s2:
            least_subject2 = subjectName.s3
        if sub4==l_s2:
            least_subject2 = subjectName.s4
        if sub5==l_s2:
            least_subject2 = subjectName.s5
        if sub6==l_s2:
            least_subject2 = subjectName.s6
        if sub7==l_s2:
            least_subject2 = subjectName.s7
        if sub8==l_s2:
            least_subject2 = subjectName.s8
        print(least_subject2)

        if sub1==l_s3:
                least_subject3 = subjectName.s1
        if sub2==l_s3:
            least_subject3 = subjectName.s2
        if sub3==l_s3:
            least_subject3 = subjectName.s3
        if sub4==l_s3:
            least_subject3 = subjectName.s4
        if sub5==l_s3:
            least_subject3 = subjectName.s5
        if sub6==l_s3:
            least_subject3 = subjectName.s6
        if sub7==l_s3:
            least_subject3 = subjectName.s7
        if sub8==l_s3:
            least_subject3 = subjectName.s8
        print(least_subject3)

        subjects = [least_subject1,least_subject2,least_subject3]
        context={
            'Subjects' : subjects
        }
        
        return render(request, 'suggestions.html',context)
