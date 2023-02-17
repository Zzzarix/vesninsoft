from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponse, HttpResponseNotFound
from django.contrib.auth import login as auth_user, logout as auth_logout
from django.contrib.auth.hashers import make_password
from .forms import *
from .backend import *

# Create your views here.
def account(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')
    companies = set([s.registry.company for s in PayslipSheet.objects.filter(phone=request.user.phone).all()])
    return render(request, 'account.html', {'user': request.user, 'companies': companies})

def login(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account')
    form = LoginForm()
    if request.method == 'POST':
        data = request.POST.copy()
        if not data['username'].startswith('+7'):
            data['username'] = data['username'].replace('8', '+7', 1).replace(' ', '').replace('-', '')[:12]
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
            data['phone'] = data['phone'].replace('8', '+7', 1).replace(' ', '').replace('-', '')[:12]
        data['password'] = make_password(data['password'])
        form = RegistrationForm(data=data)
        if form.is_valid():
            user = form.save(True)
            auth_user(request, user)
            return HttpResponseRedirect('/account')
    return render(request, 'registration.html', {'form': form})

def logout(request: HttpRequest):
    auth_logout(request)
    return render(request, 'logout.html')

def payslips(request: HttpRequest, inn: int = None, id: int = None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')
    
    if id:
        # company = Company.objects.get(inn=inn)
        # registry = PayslipRegistry.objects.get(company=company, year=year, month=month)
        # sheet = PayslipSheet.objects.get(registry=registry, phone=request.user.phone)
        registry = PayslipRegistry.objects.get(id=id)
        sheet = PayslipSheet.objects.get(registry=registry, phone=request.user.phone)
        return render(request, 'payslips.html', {'sheet': sheet})
    elif inn:
        # company = Company.objects.get(inn=inn)
        registers = set([sheet.registry for sheet in PayslipSheet.objects.filter(phone=request.user.phone).all() if sheet.registry.company.inn == inn])
        return render(request, 'payslips.html', {'registers': registers, 'company_inn': inn})
    else:
        companies = set([s.registry.company for s in PayslipSheet.objects.filter(phone=request.user.phone).all()])
        return render(request, 'payslips.html', {'companies': companies})

def apiCreatePayslips(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseNotFound()

    data = request.POST.copy()
    content = data.get('content', None)
    if not content:
        return HttpResponseBadRequest()
    try:
        parse_payslip_registry(content)
        return HttpResponse()
    except Exception:
        return HttpResponseServerError()
