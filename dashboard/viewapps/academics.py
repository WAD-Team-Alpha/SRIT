from .helpers import *

def calculateRank(sem_no, branch, rollnum):
    students = Student.objects.all().filter(sem_no=sem_no, branch=branch)
    quizResults = []
    for i in students:
        quizResults.append(Marks.objects.all().filter(sem_no=sem_no, roll_no=i.roll_no, type=4).get())
    
    marks = [[], [], [], [], [], [], [], []]
    rank = {}

    if sem_no == 8:
        for i in range(2):
            for j in quizResults:
                js = {'j.s1': j.s1, 'j.s2': j.s2}
                marks[i].append({'roll_no': j.roll_no, 's{n}'.format(n=i+1): js['j.s{n}'.format(n=i+1)]})

        for i in range(2):
            marks[i] = sorted(marks[i], key = lambda m: m['s{n}'.format(n=i+1)], reverse=True)

        for i in range(2):
            for j in range(len(marks[i])):
                if marks[i][j]['roll_no'] == rollnum:
                    rank['s{n}'.format(n=i+1)] = j+1
                    break
    else:
        for i in range(8):
            for j in quizResults:
                js = {'j.s1': j.s1, 'j.s2': j.s2, 'j.s3': j.s3, 'j.s4': j.s4, 'j.s5': j.s5, 
                'j.s6': j.s6, 'j.s7': j.s7, 'j.s8': j.s8}
                marks[i].append({'roll_no': j.roll_no, 's{n}'.format(n=i+1): js['j.s{n}'.format(n=i+1)]})

        for i in range(8):
            marks[i] = sorted(marks[i], key = lambda m: m['s{n}'.format(n=i+1)], reverse=True)

        for i in range(8):
            for j in range(len(marks[i])):
                if marks[i][j]['roll_no'] == rollnum:
                    rank['s{n}'.format(n=i+1)] = j+1
                    break

    return rank

def academicsApp(request):
    student = Student.objects.all().filter(usr_nm=request.user.username).get()
    rollnum = student.roll_no
    semNum = student.sem_no
    print(semNum)
    quizMarks = Marks.objects.all().filter(
        roll_no=rollnum, sem_no=semNum, type=4).get()
    rollnum = student.roll_no
    semNum = student.sem_no
    branch = student.branch
    subjectName = Semester.objects.all().filter(
        roll_no=rollnum, sem_no=semNum,).get()
    id = {
        'id1': 1,
        'id2': 2,
        'id3': 3,
        'id4': 4,
        'id5': 5,
        'id6': 6,
        'id7': 7,
        'id8': 8,
    }
    rank = calculateRank(semNum, branch, rollnum)
    return render(request, 'academics.html', {'subject': subjectName, 'id': id, 'quizMarks': quizMarks, 'rank': rank})