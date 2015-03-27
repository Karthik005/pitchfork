from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from users.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import models as moder
from django.core.exceptions import *
from django.db import *
from django.contrib.auth.hashers import *


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login_view(request):
    context={'headval':"Login"}
    return render(request, 'users/login.html', context)

def login_validate(request):
    usern = request.POST.get('username',None)
    passwd = request.POST.get('password', None)
    user = authenticate(username=usern, password=passwd)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            login(request, user)
            return HttpResponse("true")
        else:
            return HttpResponse("false")
    else:
        # the authentication system was unable to verify the username and password
        return HttpResponse("false")

def register_view(request):
    if request.user.is_authenticated():
        loggedin = True
    else:
        loggedin = False
    prog_lang_list = Programming_language.objects.all()
    context={'headval' : "Register",
              'prog_lang_list': prog_lang_list,
              'loggedin' : loggedin}
    return render(request, 'users/register.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('http://localhost:8000/users/login/')



def register_validate(request):

    if request.user.is_authenticated():
        return
    
    if request.method == "GET":
        usern=request.GET.get('username',None)
        if usern is not None:
            return "username_taken"
        else:
            return "true"
            
    if request.method == "POST":
    
        usern = request.POST.get('username',None)
        passwd = request.POST.get('password', None)
        firstn = request.POST.get('firstname', None)
        lastn = request.POST.get('lastname', None)
        mail = request.POST.get('email', None)

        user = moder.User(username=usern, 
                password=passwd, 
                first_name=firstn, 
                last_name=lastn, 
                email=mail)
        
        try:
            user.save()
        except IntegrityError:
            return HttpResponse("username_taken")
        except DatabaseError:
            return HttpResponse("dberror")

        dob=request.POST.get('dob', None)
        education=request.POST.get('education', None)
        experience=request.POST.get('experience', None)
        #pls=request.POST.getlist('proglangs')


        new_detail = models.detail( user_ref = user,
                        date_of_birth = dob, 
                        educational_qualifications = education,
                        experience=experience)

        new_detail.save()

        # for i in pls:
        #     new_detail.prog_langs.add(i)
        
        return HttpResponse("true")

