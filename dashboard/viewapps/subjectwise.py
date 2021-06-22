from .helpers import *

def subjectWiseApp(request):
    
    student = Student.objects.all().filter(usr_nm=request.user.username).get()

    rollnum = student.roll_no
    semNum = student.sem_no
    subjectName = Semester.objects.all().filter(
        roll_no=rollnum, sem_no=semNum,).get()

    m1 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=0).get()
    m2 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=1).get()
    quiz = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=4).get()

    m1t = m1.s1 + m1.s2 + m1.s3 + m1.s4 + m1.s5 + m1.s6 + m1.s7 + m1.s8
    m2t = m2.s1 + m2.s2 + m2.s3 + m2.s4 + m2.s5 + m2.s6 + m2.s7 + m2.s8
    qt = quiz.s1 + quiz.s2 + quiz.s3 + quiz.s4 + quiz.s5 + quiz.s6 + quiz.s7 + quiz.s8

    flag = m1t + m2t + qt

    if flag == 0:
        return render(request, 'subjectwise.html', {'flag': flag})

    savePieChart(m1.s1, m2.s1, quiz.s1,
                 'image1', subjectName.s1)
    savePieChart(m1.s2, m2.s2, quiz.s2,
                 'image2', subjectName.s2)
    if semNum != 8:
        savePieChart(m1.s3, m2.s3, quiz.s3,
                      'image3', subjectName.s3)
        savePieChart(m1.s4, m2.s4, quiz.s4,
                      'image4', subjectName.s4)
        savePieChart(m1.s5, m2.s5, quiz.s5,
                      'image5', subjectName.s5)
        savePieChart(m1.s6, m2.s6, quiz.s6,
                      'image6', subjectName.s6)
        savePieChart(m1.s7, m2.s7, quiz.s7,
                      'image7', subjectName.s7)
        savePieChart(m1.s8, m2.s8, quiz.s8,
                      'image8', subjectName.s8)
    else:
        pass

    return render(request, 'subjectwise.html', {'subjectName': subjectName, 'flag': flag})