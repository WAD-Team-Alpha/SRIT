from dashboard.viewapps.dashboard import dashboardApp
from dashboard.viewapps.suggestion import suggestionApp
from dashboard.viewapps.report import reportApp
from dashboard.viewapps.overall import overallApp
from dashboard.viewapps.subjectwise import subjectWiseApp
from dashboard.viewapps.academics import academicsApp
from dashboard.viewapps.quizfun import quizfunApp
from dashboard.viewapps.previoussemmarks import previousmarksApp
from dashboard.viewapps.selectprevioussem import selectprevioussemApp
from dashboard.viewapps.marks import marksApp

selectedPrevSem = ''

def dashboard(request):
    return dashboardApp(request)


def marks(request):
    return marksApp(request)

def previoussemNo(request):
    global selectedPrevSem
    renderObj, sem_no = selectprevioussemApp(request)
    selectedPrevSem = sem_no
    return renderObj



def previousmarks(request):
    global selectedPrevSem
    renderObj = previousmarksApp(request, selectedPrevSem)
    selectedPrevSem = ''
    return renderObj


def quizfun(request, subject_id):
    return quizfunApp(request, subject_id)


def academics(request):
    return academicsApp(request)


def subjectWise(request):
    return subjectWiseApp(request)


def overall(request):
    return overallApp(request)


def report(request):
    return reportApp(request)


def suggestion(request):
    return suggestionApp(request)    