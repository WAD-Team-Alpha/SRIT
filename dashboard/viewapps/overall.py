from .helpers import *


def overallApp(request):
    student = Student.objects.all().filter(
        usr_nm=request.user.username).get()
    rollnum = student.roll_no
    semNum = student.sem_no
    subjectName = Semester.objects.all().filter(
        roll_no=rollnum, sem_no=semNum,).get()
    m1 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=0).get()
    m2 = Marks.objects.all().filter(roll_no=rollnum, sem_no=semNum, type=1).get()

    subject1 = (m1.s1 + m2.s1)*100/60
    subject2 = (m1.s2 + m2.s2)*100/60
    if semNum != 8:
        subject3 = (m1.s3 + m2.s3)*100/60
        subject5 = (m1.s5 + m2.s5)*100/60
        subject4 = (m1.s4 + m2.s4)*100/60
        subject6 = (m1.s6 + m2.s6)*100/60
        subject7 = (m1.s7 + m2.s7)*100/60
        subject8 = (m1.s8 + m2.s8)*100/60
    else:
        pass

    if semNum != 8:
        marks = [subject1, subject2, subject3, subject4,
                 subject5, subject6, subject7, subject8]
        subjectNames = [subjectName.s1, subjectName.s2, subjectName.s3,
                        subjectName.s4, subjectName.s5, subjectName.s6, subjectName.s7, subjectName.s8]
    else:
        marks = [subject1, subject2]
        subjectNames = [subjectName.s1, subjectName.s2]

    courses = subjectNames
    values = marks
    subjectsDict = []
    for x in courses:
        dict = {}
        dict['fn'] = x
        dict['sn'] = name(x)
        subjectsDict.append(dict)
    courses = [name(x) for x in courses]
    fig = plt.figure(figsize=(10, 5))
    my_colors = ['red', 'blue', 'green', 'cyan', 'Purple', 'pink']
    # creating the bar plot

    graph = plt.bar(courses, values, color=my_colors,
                    width=0.2)

    plt.xlabel("Subjects")
    plt.ylabel("Score in Each Subject")
    plt.title("Overall Trends")

    Percentage = []
    if sum(values) != 0:
        for i in range(len(values)):
            pct = (values[i] / sum(values)) * 100
            Percentage.append(round(pct, 2))
    else:
        for i in range(len(values)):

            Percentage.append(0.00)

    i = 0
    for p in graph:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        plt.text(x+width/2,
                 y+height*1.01,
                 str(Percentage[i])+'%',
                 ha='center',
                 weight='bold')
        i += 1
    plt.savefig('media/overall_barchart.png', dpi=100)

    plt.close()
    flag1 = sum(values)
    # skill wise analysis
    group = CSE
    if student.branch == 'CSE':
        group = CSE
    elif student.branch == 'EEE':
        group = EEE
    elif student.branch == 'MECH' or student.branch == 'CVIL':
        group = MECH
    elif student.branch == 'ECE':
        group = ECE

    divisions = list(group.keys())

    newdivisions = [name(x) for x in divisions]
    divisionsDict = []
    for x in divisions:
        dict = {}
        dict['fn'] = x
        dict['sn'] = name(x)
        divisionsDict.append(dict)

    scores = []
    for x in group:
        scores.append(calculateTotal(student, group[x]))
    fig = plt.figure(figsize=(10, 5))
    graph = plt.bar(newdivisions, scores, color=my_colors,
                    width=0.2)

    plt.xlabel("Skills")
    plt.ylabel("Score in Each Skill")
    plt.title("Skill Wise Analysis")
    Percentage = []
    if sum(scores) != 0:
        for i in range(len(scores)):
            pct = (scores[i] / sum(scores)) * 100
            Percentage.append(round(pct, 2))
    else:
        for i in range(len(scores)):

            Percentage.append(0.00)

    i = 0
    for p in graph:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        plt.text(x+width/2,
                 y+height*1.01,
                 str(Percentage[i])+'%',
                 ha='center',
                 weight='bold')
        i += 1
    plt.savefig('media/skillwise_barchart.png', dpi=100)

    plt.close()
    flag2 = sum(scores)
    return render(request, 'overall.html', {'shortcuts': divisionsDict, 'subjectsDict': subjectsDict, 'flag1': flag1, 'flag2': flag2})
