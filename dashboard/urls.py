from django.urls import path
from dashboard import views

urlpatterns = [
    path('home/', views.dashboard, name='home'),
]