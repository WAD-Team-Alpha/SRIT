from .helpers import *
from ..CSE import *


def returnquestions(subjectname, sem_no):
    questions = []

    if sem_no == 1:
        questions = sem_1
    elif sem_no == 2:
        questions = sem_2
    elif sem_no == 3:
        questions = sem_3
    elif sem_no == 4:
        questions = sem_4
    elif sem_no == 5:
        questions = sem_5
    elif sem_no == 6:
        questions = sem_6
    elif sem_no == 7:
        questions = sem_7
    elif sem_no == 8:
        questions = sem_8

    for quiz in questions:
        if quiz['subject_name'] == subjectname:
            print(quiz['subject_name'])
            return quiz['QUESTIONS']


def findSubject(rollnum, sem_no, id):
    subjects = Semester.objects.all().filter(roll_no=rollnum, sem_no=sem_no).get()
    subjectName = ""
    if id == 1:
        subjectName = subjects.s1
    elif id == 2:
        subjectName = subjects.s2
    elif id == 3:
        subjectName = subjects.s3
    elif id == 4:
        subjectName = subjects.s4
    elif id == 5:
        subjectName = subjects.s5
    elif id == 6:
        subjectName = subjects.s6
    elif id == 7:
        subjectName = subjects.s7
    elif id == 8:
        subjectName = subjects.s8

    return returnquestions(subjectName, sem_no)


def quizfunApp(request, subject_id):
    student = Student.objects.all().filter(usr_nm=request.user.username).get()
    rollnum = student.roll_no
    semNum = student.sem_no

    if request.method == 'POST':
        questions = findSubject(rollnum, semNum, subject_id)
        score = 0
        # print(validate(request.POST['question1'], request.POST['q1']))
        if validate(request.POST['question1'], request.POST['q1'], questions):
            score += 2
            print("q1", score)
        if validate(request.POST['question2'], request.POST['q2'], questions):
            score += 2
            print("q2", score)
        if validate(request.POST['question3'], request.POST['q3'], questions):
            score += 2
            print("q3", score)
        if validate(request.POST['question4'], request.POST['q4'], questions):
            score += 2
            print("q4", score)
        if validate(request.POST['question5'], request.POST['q5'], questions):
            score += 2
            print("q5", score)
        updateQuizMarks(subject_id, score, semNum, rollnum)

        return redirect('academics')

    # student = Student.objects.all().filter(usr_nm=request.user.username).get()
    questions = findSubject(rollnum, semNum, subject_id)
    selectedQuestions = random.sample(questions, 5)
    question0 = selectedQuestions[0]

    question1 = selectedQuestions[1]
    question2 = selectedQuestions[2]
    question3 = selectedQuestions[3]
    question4 = selectedQuestions[4]
    selectedQuestions = {
        'question0': question0,
        'question1': question1,
        'question2': question2,
        'question3': question3,
        'question4': question4,
    }
    id = subject_id
    return render(request, 'quiz.html', {'questions': selectedQuestions, 'student': student, 'id': id})
