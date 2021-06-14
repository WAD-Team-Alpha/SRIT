from authpage.views import *
from authpage.eee import *
from authpage.mech import *
from authpage.ece import *
from authpage.cse import *
from authpage.models import Student
from .models import *
from django.core.files.storage import FileSystemStorage
import numpy as np
from matplotlib import pyplot as plt
from django.shortcuts import render, redirect
# import random
import matplotlib
matplotlib.use('Agg')
# Create your views here.

selectedPrevSem = ''


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


def calculateInternal(mid1, mid2, sem_no):
    internal = []
    if sem_no == 8:
        m1 = [int(mid1.s1), int(mid1.s2)]
        m2 = [int(mid2.s1), int(mid2.s2)]
    else:
        m1 = [int(mid1.s1), int(mid1.s2), int(mid1.s3), int(mid1.s4),
              int(mid1.s5), int(mid1.s6), int(mid1.s7), int(mid1.s8)]
        m2 = [int(mid2.s1), int(mid2.s2), int(mid2.s3), int(mid2.s4),
              int(mid2.s5), int(mid2.s6), int(mid2.s7), int(mid2.s8)]

    m = zip(m1, m2)

    for i, j in m:
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


def calculateCsp(marks, sem_no):
    if sem_no == 8:
        internal = [int(marks['is1']), int(marks['is2'])]
        external = [int(marks['es1']), int(marks['es2'])]
    else:
        internal = [int(marks['is1']), int(marks['is2']), int(marks['is3']), int(
            marks['is4']), int(marks['is5']), int(marks['is6']), int(marks['is7']), int(marks['is8'])]
        external = [int(marks['es1']), int(marks['es2']), int(marks['es3']), int(
            marks['es4']), int(marks['es5']), int(marks['es6']), int(marks['es7']), int(marks['es8'])]

    total = zip(internal, external)
    c = 0
    for i, j in total:
        c = c+i+j

    if sem_no == 8:
        c = c/2
    else:
        c = c/8

    return c


def marks(request):
    if request.method == "POST":
        marks = request.POST
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        rollnum = student.roll_no
        sem_no = student.sem_no

        for i in range(2):
            if sem_no == 8:
                Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=i).update(
                    s1=marks['s1m{j}'.format(j=i+1)],
                    s2=marks['s2m{j}'.format(j=i+1)],
                )
            else:
                Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=i).update(
                    s1=marks['s1m{j}'.format(j=i+1)],
                    s2=marks['s2m{j}'.format(j=i+1)],
                    s3=marks['s3m{j}'.format(j=i+1)],
                    s4=marks['s4m{j}'.format(j=i+1)],
                    s5=marks['s5m{j}'.format(j=i+1)],
                    s6=marks['s6m{j}'.format(j=i+1)],
                    s7=marks['s7m{j}'.format(j=i+1)],
                    s8=marks['s8m{j}'.format(j=i+1)]
                )

        mid1 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=0).get()
        mid2 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=1).get()

        internal = calculateInternal(mid1, mid2, sem_no)
        external = predictExternal(internal)

        if sem_no == 8:
            updateMarks(sem_no, rollnum, 2, internal[0], internal[1])
            updateMarks(sem_no, rollnum, 3, external[0], external[1])
        else:
            updateMarks(sem_no, rollnum, 2, internal[0], internal[1], internal[2],
                        internal[3], internal[4], internal[5], internal[6], internal[7])
            updateMarks(sem_no, rollnum, 3, external[0], external[1], external[2],
                        external[3], external[4], external[5], external[6], external[7])

        mid1 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=0).get()
        mid2 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=1).get()
        ext = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=3).get()
        sub = Semester.objects.all().filter(
            sem_no=sem_no, roll_no=rollnum, status=0).get()

        return render(request, 'current_marks.html', {'m1': mid1, 'm2': mid2, 'e': ext, 's': sub})
    else:
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        rollnum = student.roll_no
        sem_no = student.sem_no
        mid1 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=0).get()
        mid2 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=1).get()
        ext = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=3).get()
        sub = Semester.objects.all().filter(
            sem_no=sem_no, roll_no=rollnum, status=0).get()

        return render(request, 'current_marks.html', {'m1': mid1, 'm2': mid2, 'e': ext, 's': sub})


def previoussemNo(request):
    global selectedPrevSem
    if request.method == 'POST':
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        rollnum = student.roll_no
        branch = student.branch
        selectedPrevSem = request.POST['mdd']

        if not Semester.objects.all().filter(sem_no=selectedPrevSem, roll_no=rollnum).exists():
            if branch == 'CSE':
                createSemester(cse, selectedPrevSem, rollnum, 1)
            elif branch == 'ECE':
                createSemester(ece, selectedPrevSem, rollnum, 1)
            elif branch == 'MECH':
                createSemester(mech, selectedPrevSem, rollnum, 1)
            elif branch == 'CIVIL':
                createSemester(civil, selectedPrevSem, rollnum, 1)
            else:
                createSemester(eee, selectedPrevSem, rollnum, 1)

        if not Marks.objects.all().filter(sem_no=selectedPrevSem, roll_no=rollnum, type=2).exists():
            createMarks(selectedPrevSem, rollnum, type=2)
        if not Marks.objects.all().filter(sem_no=selectedPrevSem, roll_no=rollnum, type=3).exists():
            createMarks(selectedPrevSem, rollnum, type=3)

        sem = Semester.objects.all().filter(sem_no=selectedPrevSem, roll_no=rollnum).get()
        j = Marks.objects.all().filter(sem_no=selectedPrevSem,
                                       roll_no=rollnum, type=2).get()
        e = Marks.objects.all().filter(sem_no=selectedPrevSem,
                                       roll_no=rollnum, type=3).get()

        obj = ''
        for i in range(int(student.sem_no)):
            obj = obj + str(i+1)

        return render(request, 'previous_marks.html', {'sub': sem, 'i': j, 'e': e, 'sems': obj, 'cs': selectedPrevSem})


def previousmarks(request):
    global selectedPrevSem
    if request.method == 'POST':
        print(selectedPrevSem)
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        rollnum = student.roll_no
        branch = student.branch
        marks = request.POST

        isExists = False
        if Semester.objects.all().filter(sem_no=selectedPrevSem, roll_no=rollnum).exists():
            isExists = True

        if isExists:
            if selectedPrevSem == '8':
                updateMarks(selectedPrevSem, rollnum, 2,
                            marks['is1'], marks['is2'])
                updateMarks(selectedPrevSem, rollnum, 3,
                            marks['es1'], marks['es2'])
            else:
                updateMarks(selectedPrevSem, rollnum, 2, marks['is1'], marks['is2'], marks['is3'],
                            marks['is4'], marks['is5'], marks['is6'], marks['is7'], marks['is8'])
                updateMarks(selectedPrevSem, rollnum, 3, marks['es1'], marks['es2'], marks['es3'],
                            marks['es4'], marks['es5'], marks['es6'], marks['es7'], marks['es8'])
        else:
            if selectedPrevSem == '8':
                createMarks(selectedPrevSem, rollnum, 2,
                            marks['is1'], marks['is2'])
                createMarks(selectedPrevSem, rollnum, 3,
                            marks['es1'], marks['es2'])
            else:
                createMarks(selectedPrevSem, rollnum, 2, marks['is1'], marks['is2'], marks['is3'],
                            marks['is4'], marks['is5'], marks['is6'], marks['is7'], marks['is8'])
                createMarks(selectedPrevSem, rollnum, 3, marks['es1'], marks['es2'], marks['es3'],
                            marks['es4'], marks['es5'], marks['es6'], marks['es7'], marks['es8'])

        cur_per = calculateCsp(marks, student.sem_no)

        print(type(selectedPrevSem))

        if selectedPrevSem == '8':
            if branch == 'CSE':
                if isExists:
                    updateSemester8(cse, selectedPrevSem, rollnum, 1, cur_per)
                else:
                    createSemester8(cse, selectedPrevSem, rollnum, 1, cur_per)
            elif branch == 'ECE':
                if isExists:
                    updateSemester8(ece, selectedPrevSem, rollnum, 1, cur_per)
                else:
                    createSemester8(ece, selectedPrevSem, rollnum, 1, cur_per)
            elif branch == 'MECH':
                if isExists:
                    updateSemester8(mech, selectedPrevSem, rollnum, 1, cur_per)
                else:
                    createSemester8(mech, selectedPrevSem, rollnum, 1, cur_per)
            elif branch == 'CIVIL':
                if isExists:
                    updateSemester8(civil, selectedPrevSem,
                                    rollnum, 1, cur_per)
                else:
                    createSemester8(civil, selectedPrevSem,
                                    rollnum, 1, cur_per)
            else:
                if isExists:
                    updateSemester8(eee, selectedPrevSem, rollnum, 1, cur_per)
                else:
                    createSemester8(eee, selectedPrevSem, rollnum, 1, cur_per)
        else:
            if branch == 'CSE':
                if isExists:
                    updateSemester(cse, selectedPrevSem, rollnum, 1, cur_per)
                else:
                    createSemester(cse, selectedPrevSem, rollnum, 1, cur_per)
            elif branch == 'ECE':
                if isExists:
                    updateSemester(ece, selectedPrevSem, rollnum, 1, cur_per)
                else:
                    createSemester(ece, selectedPrevSem, rollnum, 1, cur_per)
            elif branch == 'MECH':
                if isExists:
                    updateSemester(mech, selectedPrevSem, rollnum, 1, cur_per)
                else:
                    createSemester(mech, selectedPrevSem, rollnum, 1, cur_per)
            elif branch == 'CIVIL':
                if isExists:
                    updateSemester(civil, selectedPrevSem, rollnum, 1, cur_per)
                else:
                    createSemester(civil, selectedPrevSem, rollnum, 1, cur_per)
            else:
                if isExists:
                    updateSemester(eee, selectedPrevSem, rollnum, 1, cur_per)
                else:
                    createSemester(eee, selectedPrevSem, rollnum, 1, cur_per)

        sem = Semester.objects.all().filter(sem_no=selectedPrevSem, roll_no=rollnum).get()
        j = Marks.objects.all().filter(sem_no=selectedPrevSem,
                                       roll_no=rollnum, type=2).get()
        e = Marks.objects.all().filter(sem_no=selectedPrevSem,
                                       roll_no=rollnum, type=3).get()

        obj = ''
        for i in range(int(student.sem_no)):
            obj = obj + str(i+1)

        if str(student.sem_no) == str(selectedPrevSem):
            if selectedPrevSem == '8':
                # messages
                return redirect('home')
            else:
                Student.objects.all().filter(roll_no=rollnum).update(sem_no=student.sem_no + 1)
                if branch == 'CSE':
                    createSemester(cse, student.sem_no + 1, rollnum, 1)
                elif branch == 'ECE':
                    createSemester(ece, student.sem_no + 1, rollnum, 1)
                elif branch == 'MECH':
                    createSemester(mech, student.sem_no + 1, rollnum, 1)
                elif branch == 'CIVIL':
                    createSemester(civil, student.sem_no + 1, rollnum, 1)
                else:
                    createSemester(eee, student.sem_no + 1, rollnum, 1)

        return render(request, 'previous_marks.html', {'sub': sem, 'i': j, 'e': e, 'sems': obj, 'cs': selectedPrevSem})

    else:
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        sem = Semester.objects.all().filter(
            sem_no=student.sem_no, roll_no=student.roll_no).get()
        j = Marks.objects.all().filter(sem_no=student.sem_no,
                                       roll_no=student.roll_no, type=2).get()
        e = Marks.objects.all().filter(sem_no=student.sem_no,
                                       roll_no=student.roll_no, type=3).get()
        rollnum = student.roll_no
        sem_no = student.sem_no
        obj = ''
        for i in range(int(sem_no)):
            obj = obj + str(i+1)

        return render(request, 'previous_marks.html', {'sub': sem, 'i': j, 'e': e, 'sems': obj, 'cs': str(sem_no)})


def activities(request):
    student = Student.objects.all().filter(Username=request.user.username).get()

    rollnum = student.roll_no
    semNum = Student.sem_no
    subjectName = Semester.objects.all().filter(
        roll_no=rollnum, sem_no=semNum,).get()
    quiz = [
        {
            'subjectName': subjectName.s1,
            'id': 1
        },
        {
            'subjectName': subjectName.s2,
            'id': 2
        },
        {
            'subjectName': subjectName.s3,
            'id': 3
        },
        {
            'subjectName': subjectName.s4,
            'id': 4
        },
        {
            'subjectName': subjectName.s5,
            'id': 5
        },
        {
            'subjectName': subjectName.s6,
            'id': 6
        },
        {
            'subjectName': subjectName.s7,
            'id': 7
        },
        {
            'subjectName': subjectName.s8,
            'id': 8
        },
    ]
    return render(request, 'academics.html', {'quiz': quiz})


def savePieChart(m1, m2, quiz, extra_curricular, imgName, subjectName):
    if m1 == 0 and m2 == 0 and quiz == 0:
        labels = '', '', '', ''
    else:
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

    student = Student.objects.all().filter(usr_nm=request.user.username).get()

    rollnum = student.roll_no
    semNum = student.sem_no
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

    return render(request, 'subjectwise.html', {'subjectName': subjectName})


def overall(request):
    student = Student.objects.all().filter(
        usr_nm=request.user.username).get()
    rollnum = student.roll_no
    semNum = student.sem_no
    subjectName = Semester.objects.all().filter(
        roll_no=rollnum, sem_no=semNum,).get()
    m1 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=0).get()
    m2 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=1).get()
    quiz = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).get()
    extra_curricular = Marks.objects.all().filter(
        roll_no=rollnum, sem_no=semNum, type=5).get()
    subject1 = (m1.s1 + m2.s1)*100/60
    subject2 = (m1.s2 + m2.s2)*100/60
    if semNum != 8:
        subject3 = (m1.s3 + m2.s3)*100/60
        subject5 = (m1.s5 + m2.s5)*100/60
        subject4 = (m1.s4 + m2.s4)*100/60
        subject6 = (m1.s6 + m2.s6)*100/60
        subject7 = (m1.s7 + m2.s7)*100/60
        subject8 = (m1.s8 + m2.s8)*100/60
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
    return render(request, 'report.html')


def suggestion(request):
    return render(request, 'suggestion.html')
