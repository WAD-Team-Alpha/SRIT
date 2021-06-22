from .helpers import *

def academicsApp(request):
    student = Student.objects.all().filter(usr_nm=request.user.username).get()
    rollnum = student.roll_no
    semNum = student.sem_no
    quizMarks = Marks.objects.all().filter(
        roll_no=rollnum, sem_no=semNum, type=4).get()
    rollnum = student.roll_no
    semNum = student.sem_no
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
    return render(request, 'academics.html', {'subject': subjectName, 'id': id, 'quizMarks': quizMarks})