from django.shortcuts import render
from django.http import HttpResponse
from users.models import *
from django.contrib.auth import authenticate

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    context={'headval':"Login"}
    return render(request, 'users/login.html', context)

def login_validate(request):
    usern = request.POST.get('username',None)
    passwd = request.POST.get('password', None)
    user = authenticate(username=usern, password=passwd)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            return HttpResponse("true")
        else:
            return HttpResponse("false")
    else:
        # the authentication system was unable to verify the username and password
        return HttpResponse("false")

def register(request):
    context={'headval' : "Register"}
    return render(request)