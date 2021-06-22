from django.urls import path
from authpage import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('security_check/', views.securityCheck, name='security_code'),
    path('forgot_password/', views.forgotPassword, name='forgot_password'),
]