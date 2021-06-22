from .helpers import *

def selectprevioussemApp(request):
    global selectedPrevSem
    if request.method == 'POST':
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        rollnum = student.roll_no
        branch = student.branch
        selectedPrevSem = request.POST['mdd']

        if not Semester.objects.all().filter(sem_no=selectedPrevSem, roll_no=rollnum).exists():
            if branch == 'CSE':
                createSemester(cse, selectedPrevSem, rollnum, 0)
            elif branch == 'ECE':
                createSemester(ece, selectedPrevSem, rollnum, 0)
            elif branch == 'MECH':
                createSemester(mech, selectedPrevSem, rollnum, 0)
            elif branch == 'CIVIL':
                createSemester(civil, selectedPrevSem, rollnum, 0)
            else:
                createSemester(eee, selectedPrevSem, rollnum, 0)

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

        return render(request, 'previous_marks.html', {'sub': sem, 'i': j, 'e': e, 'sems': obj, 'cs': selectedPrevSem}), selectedPrevSem