from django.urls import path
from dashboard import views

urlpatterns = [
    path('home/', views.dashboard, name='home'),
    path('currentsem/', views.marks, name='currentsem'),
    path('previoussem/', views.previousmarks, name='previoussem'),
    path('suggestions/',views.suggestion,name='suggestions'),
    path('report/',views.report,name='report')
]