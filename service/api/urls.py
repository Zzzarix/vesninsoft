from django.urls import path, include
from django.contrib.auth import views as auth_views

from api import views

urlpatterns = [
    path('salaryReport/', views.apiSalaryReport, name='salaryReport'),
    path('addOrg/', views.apiAddOrg, name='addOrg'),
]
