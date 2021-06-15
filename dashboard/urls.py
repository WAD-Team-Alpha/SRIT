from test import name
from django.urls import path
from dashboard import views

urlpatterns = [
    path('home/', views.dashboard, name='home'),
    path('currentsem/', views.marks, name='currentsem'),
    path('previoussem/', views.previousmarks, name='previoussem'),
    path('subjectwise/', views.subjectWise, name='subjectwise'),
    path('overall/', views.overall, name='overall'),
    path('academics/', views.academics, name='academics'),
    #
    path('<int:subject_id>', views.quizfun, name='quizfun'),
    path('previoussemnumber/', views.previoussemNo, name='previoussemnumber'),
]
