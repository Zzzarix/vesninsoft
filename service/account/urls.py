from django.urls import path, include
from django.contrib.auth import views as auth_views
from .forms import LoginForm

from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('payslips/', views.payslips, name='payslips')
]
