from django.urls import path, include
from django.contrib.auth import views as auth_views
from .forms import LoginForm

from . import views
from . import api

urlpatterns = [
    path('', views.account, name='account'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('payslips/', views.payslips, name='payslips_companies'),
    path('payslips/<int:inn>/', views.payslips, name='payslips_sheets'),
    # path('payslips/{int:inn}/{int:year}/{year:month}', views.payslips, name='payslips'),
    path('payslips/<int:inn>/<int:id>/', views.payslips, name='payslips_view'),
]
 