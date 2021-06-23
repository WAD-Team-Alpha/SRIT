# Helper functions are written here

from .quizz import quiz
from .models import *
import numpy as np
from matplotlib import pyplot as plt
import random
import matplotlib
matplotlib.use('Agg')


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
        external.append(1.406*i + 24.625)

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


def calculateCspCurrentSem(internal, external, sem_no):
    total = zip(internal, external)
    c = 0
    for i, j in total:
        c = c+i+j

    if sem_no == 8:
        c = c/2
    else:
        c = c/8

    return c


def validate(question, answer, quiz):
    for q in quiz:
        if question == q['question']:

            if answer == q['answer']:

                return True
    return False


def updateQuizMarks(id, score, semNum, rollnum):
    if id == 1:
        Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).update(s1=score)
    elif id == 2:
        Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).update(s2=score)
    elif id == 3:
        Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).update(s3=score)
    elif id == 4:
        Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).update(s4=score)
    elif id == 5:
        Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).update(s5=score)
    elif id == 6:
        Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).update(s6=score)
    elif id == 7:
        Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).update(s7=score)
    elif id == 8:
        Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).update(s8=score)


def savePieChart(m1, m2, quiz, imgName, subjectName):
    def func(pct, allvalues):

        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%".format(pct)

    if m1 == 0 and m2 == 0 and quiz == 0:
        labels = '', '', ''
    else:
        labels = 'mid-1', 'mid-2', 'quiz'

    sizes = [m1, m2,  quiz]
    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = (0.1, 0.1, 0.1)

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.pie(sizes, explode=explode, labels=labels, autopct=lambda pct: func(pct, sizes),
            shadow=True, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')
    plt.title("Pie chart of "+subjectName+"")
    plt.legend()
    plt.savefig('media/'+imgName+'.png', dpi=100)
    plt.close()


def name(s):

    # split the string into a list
    l = s.split()
    new = ""

    # traverse in the list
    for i in range(len(l)):
        s = l[i]

        # adds the capital first character
        new += (s[0].upper()+'.')

    # l[-1] gives last item of list l. We
    # use title to print first character in
    # capital.

    return new


def findsubjectscore(student, subject):

    semNum = student.sem_no
    rollnum = student.roll_no
    for i in range(semNum):
        if Semester.objects.all().filter(roll_no=rollnum, sem_no=i).exists():
            subjects = Semester.objects.all().filter(roll_no=rollnum, sem_no=i).get()
            if subjects.s1 == subject:
                internal = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=2).get()
                external = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=3).get()
                return internal.s1 + external.s1
            if subjects.s2 == subject:
                internal = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=2).get()
                external = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=3).get()
                return internal.s2 + external.s2
            if subjects.s3 == subject:
                internal = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=2).get()
                external = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=3).get()
                return internal.s3 + external.s3
            if subjects.s4 == subject:
                internal = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=2).get()
                external = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=3).get()
                return internal.s4 + external.s4
            if subjects.s5 == subject:
                internal = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=2).get()
                external = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=3).get()
                return internal.s5 + external.s5
            if subjects.s6 == subject:
                internal = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=2).get()
                external = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=3).get()
                return internal.s6 + external.s6
            if subjects.s7 == subject:
                internal = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=2).get()
                external = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=3).get()
                return internal.s7 + external.s7
            if subjects.s8 == subject:
                internal = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=2).get()
                external = Marks.objects.all().filter(roll_no=rollnum, sem_no=i, type=3).get()
                return internal.s8 + external.s8
    return 0


def calculateTotal(student, subjects):

    totalScore = 0
    for subject in subjects:

        totalScore += findsubjectscore(student, subject)

    return totalScore
