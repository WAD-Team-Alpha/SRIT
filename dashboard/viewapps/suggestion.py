from .helpers import *

def suggestionApp(request):
    student = Student.objects.all().filter(usr_nm=request.user.username).get()
    rollnum = student.roll_no
    semNum = student.sem_no
    subjectName = Semester.objects.all().filter(
        roll_no=rollnum, sem_no=semNum,).get()

    if semNum == 8:
        m1 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=0).get()
        m2 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=1).get()
        Subjects_names = [subjectName.s1, subjectName.s2, subjectName.s3,
                          subjectName.s4, subjectName.s5, subjectName.s6, subjectName.s7, subjectName.s8]
        sub1 = m1.s1+m2.s1
        sub2 = m1.s2+m2.s2

        if sub1 + sub2 == 0:
            return render(request, 'suggestions.html', {'flag': 0})
        
        sub = [sub1,sub2]
        total = zip(Subjects_names, sub)

        k = {}
        for i, j in total:
            k[i] = j

        l = sorted(k.items(), key=lambda x: x[1])

        print(l)

        subjects_focused = [l[0][0]]

        context = {
            'Subjects_focused': subjects_focused,
            'flag': 1
        }

        return render(request, 'suggestions.html', context)

    else:
        m1 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=0).get()
        m2 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=1).get()
        Subjects_names = [subjectName.s1, subjectName.s2, subjectName.s3,
                          subjectName.s4, subjectName.s5, subjectName.s6, subjectName.s7, subjectName.s8]

        sub1 = m1.s1+m2.s1
        sub2 = m1.s2+m2.s2
        sub3 = m1.s3+m2.s3
        sub4 = m1.s4+m2.s4
        sub5 = m1.s5+m2.s5
        sub6 = m1.s6+m2.s6
        sub7 = m1.s7+m2.s7
        sub8 = m1.s8+m2.s8

        myTotal = sub1 + sub2 + sub3 + sub4 + sub5 + sub6 + sub7 + sub8

        if myTotal == 0:
            return render(request, 'suggestions.html', {'flag': 0}) 

        sub = [sub1,sub2,sub3,sub4,sub5,sub6,sub7,sub8]
        total = zip(Subjects_names, sub)

        k = {}
        for i, j in total:
            k[i] = j

        l = sorted(k.items(), key=lambda x: x[1])

        
        
        subjects_focused = [l[0][0],l[1][0],l[2][0]]
        
        context={
            'Subjects_focused' : subjects_focused,
            'flag': 1
        }

        return render(request, 'suggestions.html', context)