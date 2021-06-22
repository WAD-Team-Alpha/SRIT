from .helpers import *

def marksApp(request):
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
        csp = calculateCspCurrentSem(internal, external, sem_no)

        Semester.objects.all().filter(roll_no=rollnum, sem_no=sem_no).update(csp=csp)

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
        print(sem_no)
        mid1 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=0).get()
        mid2 = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=1).get()
        ext = Marks.objects.all().filter(sem_no=sem_no, roll_no=rollnum, type=3).get()
        sub = Semester.objects.all().filter(sem_no=sem_no, roll_no=rollnum).get()
            
        
        return render(request, 'current_marks.html',{'m1': mid1, 'm2': mid2, 'e': ext, 's': sub})