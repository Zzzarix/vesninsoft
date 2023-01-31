from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect

def home(request: HttpRequest):
    return HttpResponseRedirect('/account')
