from .helpers import *

def previousmarksApp(request, selectedPrevSem):
    print(selectedPrevSem)
    if request.method == 'POST':
        if selectedPrevSem == '':
            messages.success(request, "Please select a sem")
            return redirect('previoussem')
        print(selectedPrevSem)
        student = Student.objects.all().filter(usr_nm=request.user.username).get()
        rollnum = student.roll_no
        branch = student.branch
        marks = request.POST

        isExists = False
        if Semester.objects.all().filter(sem_no=selectedPrevSem, roll_no=rollnum).exists():
            isExists = True

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

        cur_per = calculateCsp(marks, student.sem_no)

        print(cur_per)
        targets = Semester.objects.all().filter(sem_no=selectedPrevSem, roll_no=rollnum).get()

        if selectedPrevSem == '8':
            if branch == 'CSE':
                updateSemester8(cse, selectedPrevSem, rollnum, 1, cur_per, targets.ot)
            elif branch == 'ECE':
                updateSemester8(ece, selectedPrevSem, rollnum, 1, cur_per, targets.ot)
            elif branch == 'MECH':
                updateSemester8(mech, selectedPrevSem, rollnum, 1, cur_per, targets.ot)
            elif branch == 'CIVIL':
                updateSemester8(civil, selectedPrevSem, rollnum, 1, cur_per, targets.ot)
            else:
                updateSemester8(eee, selectedPrevSem, rollnum, 1, cur_per, targets.ot)
        else:
            if branch == 'CSE':
                updateSemester(cse, selectedPrevSem, rollnum, 1, cur_per, targets.ot)
            elif branch == 'ECE':
                updateSemester(ece, selectedPrevSem, rollnum, 1, cur_per, targets.ot)
            elif branch == 'MECH':
                updateSemester(mech, selectedPrevSem, rollnum, 1, cur_per, targets.ot)
            elif branch == 'CIVIL':
                print("I am here")
                updateSemester(civil, selectedPrevSem, rollnum, 1, cur_per, targets.ot)
            else:
                updateSemester(eee, selectedPrevSem, rollnum, 1, cur_per, targets.ot)

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
                messages.success(request, 'You have completed your graduation!!')
                return redirect('home')
            else:
                otSem = Semester.objects.all().filter(roll_no=rollnum, sem_no=student.sem_no).get()
                Student.objects.all().filter(roll_no=rollnum).update(sem_no=student.sem_no + 1)
                if student.sem_no + 1 == 8:
                    if branch == 'CSE':
                        print("i am being executed")
                        createSemester8(cse, student.sem_no + 1, rollnum, 0, 0, otSem.ot)
                    elif branch == 'ECE':
                        createSemester8(ece, student.sem_no + 1, rollnum, 0, 0, otSem.ot)
                    elif branch == 'MECH':
                        createSemester8(mech, student.sem_no + 1, rollnum, 0, 0, otSem.ot)
                    elif branch == 'CIVIL':
                        createSemester8(civil, student.sem_no + 1, rollnum, 0, 0, otSem.ot)
                    else:
                        createSemester8(eee, student.sem_no + 1, rollnum, 0, 0, otSem.ot)
                else:
                    if branch == 'CSE':
                        print("i am being executed")
                        createSemester(cse, student.sem_no + 1, rollnum, 0, 0, otSem.ot)
                    elif branch == 'ECE':
                        createSemester(ece, student.sem_no + 1, rollnum, 0, 0, otSem.ot)
                    elif branch == 'MECH':
                        createSemester(mech, student.sem_no + 1, rollnum, 0, 0, otSem.ot)
                    elif branch == 'CIVIL':
                        createSemester(civil, student.sem_no + 1, rollnum, 0, 0, otSem.ot)
                    else:
                        createSemester(eee, student.sem_no + 1, rollnum, 0, 0, otSem.ot)
                print("i am as well")
                createMarks(student.sem_no + 1, rollnum, 0)
                createMarks(student.sem_no + 1, rollnum, 1)
                createMarks(student.sem_no + 1, rollnum, 2)
                createMarks(student.sem_no + 1, rollnum, 3)
                createMarks(student.sem_no + 1, rollnum, 4)

        currentstatus = selectedPrevSem
        selectedPrevSem = ''
        return render(request, 'previous_marks.html', {'sub': sem, 'i': j, 'e': e, 'sems': obj, 'cs': currentstatus})

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
