from django.urls import path

from . import views

urlpatterns = [
    path('account/', views.account, name='account'),
    path('', views.home, name='home')
]