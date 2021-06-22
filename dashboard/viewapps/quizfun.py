from .helpers import *

def quizfunApp(request, subject_id):
    student = Student.objects.all().filter(usr_nm=request.user.username).get()
    rollnum = student.roll_no
    semNum = student.sem_no

    if request.method == 'POST':

        score = 0
        # print(validate(request.POST['question1'], request.POST['q1']))
        if validate(request.POST['question1'], request.POST['q1']):
            score += 2
        if validate(request.POST['question2'], request.POST['q2']):
            score += 2
        if validate(request.POST['question3'], request.POST['q3']):
            score += 2
        if validate(request.POST['question4'], request.POST['q4']):
            score += 2
        if validate(request.POST['question5'], request.POST['q5']):
            score += 2
        updateQuizMarks(subject_id, score, semNum, rollnum)
        print(score)
        return redirect('academics')

    student = Student.objects.all().filter(usr_nm=request.user.username).get()

    selectedQuestions = random.sample(quiz, 5)
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
