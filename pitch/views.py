from django.shortcuts import render
from users import models as user_models
from users import views as user_views
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import models as moder
from django.core.exceptions import *
from django.db import *
from django.contrib.auth.hashers import *
from django.core.urlresolvers import reverse
from pitch.models import *
from django.db.models import Model
import urllib
import datetime

# Create your views here.

def pitch_view(request):
    if request.method == "GET":
        if request.user.is_authenticated() and not request.user.is_superuser:
            loggedin = True
        else:
            loggedin = False

        prog_lang_list = user_models.Programming_language.objects.all()
        context={'headval':"Pitch",
                 'loggedin' : loggedin,
                'login_url' : reverse('login'),
                'register_url' : reverse('register'),
                'logout_url' : reverse('logout'),
                'prog_lang_list': prog_lang_list}
        return render(request, 'pitch/pitch.html', context)

    elif request.method == "POST":
        if request.user.is_authenticated() and not request.user.is_superuser:
            user = request.user
            title = request.POST.get('title', None)
            pitch_date=datetime.datetime.now().date()
            pitch_text = request.POST.get('pitch', None)
            pitch_doc = request.POST.get('file', None)
            dev_state = "Pitch"

            new_pitch = Pitch(user=user,
                title=title,
                date=pitch_date,
                pitch=pitch_text,
                document=pitch_doc,
                dev_state=dev_state
                )
            new_pitch.save()
            # try:
            #     new_pitch.save()
            # except IntegrityError:
            #     return HttpResponse("username_taken")
            # except DatabaseError:
            #     return HttpResponse("dberror")

            prog_langs=request.POST.getlist('proglangs', None)


            for i in prog_langs:
                new_pitch.prog_langs.add(user_models.Programming_language.objects.get(name=str(i)))


            appclose=user_views.dateconvert(request.POST.get('appclose', None))
            devstart=user_views.dateconvert(request.POST.get('devstart', None))
            numvol=request.POST.get('numvol', None)

            new_pitch_data = new_pitch.data_set.create()
            new_pitch_data.pitchdata_set.create(app_close_date=appclose, dev_start_date=devstart, num_vol=numvol)

            return HttpResponse("true") 

    
def pitch_validate(request):
    if request.method == "GET":
        try:
         Pitch.objects.get(title=request.GET.get('title'))

        except Pitch.DoesNotExist:
            return HttpResponse("true")

        return HttpResponse("false")


def user_pitch(request):
    if request.method == "GET":
        if request.user.is_authenticated() and not request.user.is_superuser:
            loggedin = True
            try:
                userPitches = Pitch.objects.get(user=request.user).order_by('votes')
            except Pitch.DoesNotExist:
                userPitches = None

            context={
                    'headval':"My Pitches",
                     'loggedin' : loggedin,
                    'login_url' : reverse('login'),
                    'register_url' : reverse('register'),
                    'logout_url' : reverse('logout'),
                    'prog_lang_list': prog_lang_list}

            return render(request, 'pitch/pitch.html', context)

        else:
            login_url = Model.get_absolute_url(user_views.login_view)
            return redirect(login_url+"?red="+"pitches.user_pitch")