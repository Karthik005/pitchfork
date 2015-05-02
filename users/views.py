from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from users.models import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import models as moder
from django.core.exceptions import *
from django.db import *
from django.contrib.auth.hashers import *
from django.core.urlresolvers import reverse

import datetime


#helper functions:

def dateconvert(date):
    return datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')

# Create your views here.



def login_view(request):
    redirect_url = request.GET.get('red',None)
    if request.user.is_authenticated() and not request.user.is_superuser:
        loggedin = True
    else:
        loggedin = False
    context={'headval':"Login",
             'loggedin' : loggedin,
            'login_url' : reverse('login'),
            'register_url' : reverse('register'),
            'logout_url' : reverse('logout')}

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

    if request.user.is_authenticated() and not request.user.is_superuser:
        loggedin = True
    else:
        loggedin = False
    prog_lang_list = Programming_language.objects.all()
    print reverse(login_view)
    context={'headval' : "Register",
              'prog_lang_list': prog_lang_list,
              'loggedin' : loggedin,
              'login_url' : reverse('login'),
              'register_url' : reverse('register'),
              'logout_url' : reverse('logout'),
              'pitch_url' : reverse('pitch')}
    return render(request, 'users/register.html', context)

def logout_view(request):
    logout(request)
    red=request.GET.get('red','null')
    return redirect(reverse('home'))



def register_validate(request):

    if request.method == "GET":
        if request.GET.get('username'):
            usern=request.GET.get('username')
            try:
                ret=moder.User.objects.get(username=usern)
            except moder.User.DoesNotExist:
                ret=None
            if ret is not None:
                return HttpResponse("false")
            else:
                return HttpResponse("true")

        elif request.GET.get('email'):
            mail=request.GET.get('email')
            try:
                ret=moder.User.objects.get(email=mail)
            except moder.User.DoesNotExist:
                ret=None
            if ret is not None:
                return HttpResponse("false")
            else:
                return HttpResponse("true")



def register_user(request):


    print request.POST.getlist('proglangs')

            
    if request.method == "POST":
       
        usern = request.POST.get('username',None)
        passwd = request.POST.get('password', None)
        firstn = request.POST.get('firstname', None)
        lastn = request.POST.get('lastname', None)
        mail = request.POST.get('email', None)

        dob=dateconvert(request.POST.get('dob', None))
        education=request.POST.get('education', None)
        exp=request.POST.get('experience', None)
    
        hashedpasswd = make_password(passwd, hasher='pbkdf2_sha256')
        print hashedpasswd
        if not is_password_usable(hashedpasswd):
            return HttpResponse("dberror") 

        user = moder.User(username=usern, 
                password=hashedpasswd, 
                first_name=firstn, 
                last_name=lastn,
                email=mail)

        try:
            user.save()
        except IntegrityError:
            return HttpResponse("username_taken")
        except DatabaseError:
            return HttpResponse("dberror")

        print "reaches here"
       
        new_detail = user.detail_set.create(
                    date_of_birth = dob, 
                    educational_qualifications = education,
                    experience=exp)


        
        pls=request.POST.getlist('proglangs')

        for i in pls:
            new_detail.prog_langs.add(Programming_language.objects.get(name=str(i)))

        
        return HttpResponse("true")

