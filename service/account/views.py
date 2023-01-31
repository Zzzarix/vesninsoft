from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth import login as auth_user, logout as auth_logout
from .forms import *

# Create your views here.
def account(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')
    return render(request, 'account.html', {'user': request.user})

def login(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account')
    form = LoginForm()
    if request.method == 'POST':
        data = request.POST.copy()
        if not data['username'].startswith('+7'):
            data['username'] = data['username'].replace('8', '+7', 1)
        form = LoginForm(data=data)
        if form.is_valid():
            user = form.get_user()
            auth_user(request, user)
            return HttpResponseRedirect('/account')
    return render(request, 'login.html', {'form': form})

def registration(request: HttpRequest):
    form = RegistrationForm()
    if request.method == 'POST':
        data = request.POST.copy()
        if not data['phone'].startswith('+7'):
            data['phone'] = data['phone'].replace('8', '+7', 1)
        form = RegistrationForm(data=data)
        if form.is_valid():
            user = form.save(True)
            auth_user(request, user)
            return HttpResponseRedirect('/account')
    return render(request, 'registration.html', {'form': form})

def logout(request: HttpRequest):
    auth_logout(request)
    print(request.user)
    return render(request, 'logout.html')

def payslips(request: HttpRequest):
    return render(request, 'payslips.html')
