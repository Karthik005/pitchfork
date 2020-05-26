from django.shortcuts import render
from users import models as user_models
from users import views as user_views
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import models as moder
from django.core.exceptions import *
from django.db import *
from django.contrib.auth.hashers import *
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pitch.models import *
from django.db.models import Model
from django.template import RequestContext
import urllib
import datetime

# Create your views here.

context_loggedin = {
                'pitch_url' : reverse_lazy('pitch'),
                'mypitches_url': reverse_lazy('user_pitch'),
                'otherpitches_url': reverse_lazy('other_pitch'),
                'pitchedinpitches_url': reverse_lazy('pitchedin_pitch'),
                'logout_url':reverse_lazy('logout'),
                'login_url':reverse_lazy('login'),
                'register_url':reverse_lazy('register'),
                }


def getRating(pitch):
    votes = pitch.data_set.get().votes
    if votes >= 200:
        rating = "soprano"
    if votes<200 and votes>=100:
        rating = "tenor"
    if votes<100 and votes>=0:
        rating = "baritone"
    if votes<0:
        rating = "bass"
    return rating


def pitch_view(request):
    if request.method == "GET":
        if request.user.is_authenticated() and not request.user.is_superuser:
            loggedin = True
            profile_url=reverse('profile', args = (request.user.id,))

            prog_lang_list = user_models.Programming_language.objects.all()
            context=context_loggedin.copy()
            context.update({'prog_lang_list': prog_lang_list, 'loggedin' : loggedin, 'profile_url':profile_url})
            return render(request, 'pitch/pitch.html', context)

        else:
            login_url = reverse_lazy('login')
            return redirect(login_url+"?red=pitch")


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
            profile_url=reverse('profile', args = (request.user.id,))
            try:
                userPitches = Pitch.objects.all().filter(user=request.user)
                userPitches = sorted(userPitches, key=lambda t: -t.data_set.get().votes)
                
                empty= (True if (len(userPitches) == 0) else False)

            except Pitch.DoesNotExist:
                userPitches = None
                empty = True

            if userPitches != None:
                    paginator = Paginator(userPitches, 15) 
                    page = request.GET.get('page')
                    try:
                        user_page_pitches = paginator.page(page)
                    except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                        user_page_pitches  = paginator.page(1)
                    except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                        user_page_pitches  = paginator.page(paginator.num_pages)
            else:
                user_page_pitches  = None

            context=context_loggedin.copy()
            context.update({'user_pitches': user_page_pitches,
                        'my': True,
                        'headval': "My Pitches",
                        'empty': empty, 
                        'loggedin':loggedin,
                        'profile_url':profile_url})

            return render(request, 'pitch/mypitches.html', context)

        else:
            login_url = reverse_lazy('login')
            return redirect(login_url+"?red=user_pitch")

def other_pitch(request):

    if request.method == "GET":
        if request.user.is_authenticated() and not request.user.is_superuser:
            loggedin = True
            profile_url=reverse('profile', args = (request.user.id,))
            try:
                otherPitches = filter( lambda x: x.user != request.user, Pitch.objects.all())
                otherPitches = sorted(otherPitches, key=lambda t: -t.data_set.get().votes)
                empty = False 
            except Pitch.DoesNotExist:
                otherPitches = None
                empty = True

            if otherPitches != None:
                    paginator = Paginator(otherPitches, 15) 
                    page = request.GET.get('page')
                    try:
                        other_page_pitches = paginator.page(page)
                    except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                        other_page_pitches  = paginator.page(1)
                    except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                        other_page_pitches  = paginator.page(paginator.num_pages)
            else:
                other_page_pitches  = None

             
            context=context_loggedin.copy()
            context.update({'user_pitches': other_page_pitches,
                        'my': False,
                        'empty': empty, 
                        'headval': "Others Pitches",
                        'display_pitch_url': reverse_lazy('display_pitch'),
                        'loggedin':loggedin,
                        'profile_url':profile_url})

            return render(request, 'pitch/mypitches.html', context)

        else:
            login_url = reverse_lazy('login')
            return redirect(login_url+"?red=other_pitch")

def display_pitch(request, pitch_id):
    if request.method == "GET":
        if request.user.is_authenticated() and not request.user.is_superuser:
            loggedin = True
            profile_url=reverse('profile', args = (request.user.id,))
            try:
                pitch_displayed= Pitch.objects.get(id=pitch_id)
                empty = False 
                my = (True if (pitch_displayed.user == request.user) else False)
                rating = getRating(pitch_displayed)
                prog_langs = pitch_displayed.prog_langs.all()
                pitched_in  = True if len(VolunteeredFor.objects.all().filter(user=request.user, pitch = pitch_displayed)) !=0 else False   
                voted  = True if len(VotedFor.objects.all().filter(user=request.user, pitch = pitch_displayed)) !=0 else False   
                volunteer_list = VolunteeredFor.objects.all().filter(pitch = pitch_displayed)
                dev_team = DevTeam.objects.all().filter(pitch = pitch_displayed)
                dev_flag = True if len(dev_team) !=0 else False
                comment_list = Comment.objects.all().filter(pitch = pitch_displayed)

            except Pitch.DoesNotExist:
                pitch_displayed = None
                empty = True
                my = None
                rating = None

            context=context_loggedin.copy()
            data = pitch_displayed.data_set.get()
            pitch_data = data.pitchdata_set.get()
            context.update({'pitch': pitch_displayed,
                        'data': pitch_displayed.data_set.get(),
                        'rating':rating,
                        'data':data,
                        'pitch_data':pitch_data,
                        'votes': data.upvotes-data.downvotes,
                        'empty': empty,
                        'voted': voted,
                        'pitched_in': pitched_in,
                        'volunteer_list':volunteer_list,
                        'dev_team':dev_team,
                        'dev_flag':dev_flag,
                        'headval': "View Pitch",
                        'my': my,
                        'user':request.user,
                        'comment_list':comment_list,
                        'prog_langs': prog_langs,
                        'loggedin':loggedin,
                        'profile_url':profile_url})

            return render(request, 'pitch/displaypitch.html', context, context_instance=RequestContext(request))

        else:
            login_url = reverse_lazy('login')
            display_url=reverse_lazy('display_pitch/', args=(pitch_id,))
            return redirect(login_url+"?red=/pitch/display_pitch/"+pitch_id+"/")





def vote_pitch(request):
    if request.method == "GET":
        user = request.user
        vote = request.GET.get('vote')
        try:
            pitch = Pitch.objects.get(id = request.GET.get('pitch_id'))
        except Pitch.DoesNotExist:
            return HttpResponse("Invalid pitch")

        obj= VotedFor(user = user, pitch = pitch)
        lister = VotedFor.objects.all().filter(user=user, pitch=pitch)
        if  len(lister) == 0:
            obj.save()
            data = pitch.data_set.get()
            if vote == "1":
                data.upvotes+=1
            elif vote == "-1":
                data.downvotes+=1
            data.save()
            return HttpResponse("true")

        else:
            return HttpResponse("false")


def remove_pitch(request):
    if request.method == "GET":
        user = request.user
        try:
            pitch = Pitch.objects.get(id = request.GET.get('pitch_id'), user = user)
        except Pitch.DoesNotExist:
            return HttpResponse("false")

        pitch.delete()
        return HttpResponse("true")


def pitch_in(request):
    if request.method == "GET":
        user = request.user
        try:
            pitch = Pitch.objects.get(id = request.GET.get('pitch_id'))
        except Pitch.DoesNotExist:
            return HttpResponse("Invalid pitch") 

        try:
            volunteered = VolunteeredFor.objects.get(user = user, pitch = pitch)
            return HttpResponse("false")
        except VolunteeredFor.DoesNotExist:
            new_volunteer= VolunteeredFor(user = user, pitch = pitch)
            new_volunteer.save()
            return HttpResponse("true")

def pitchedin_pitch(request):
    if request.method == "GET":
        if request.user.is_authenticated() and not request.user.is_superuser:
            loggedin = True
            profile_url=reverse('profile', args = (request.user.id,))
            try:
                pitchedinPitches = map( lambda x: x.pitch, filter( lambda x: x.user == request.user, VolunteeredFor.objects.all()))
                pitchedinPitches = sorted(pitchedinPitches, key=lambda t: -t.data_set.get().votes)
                empty = False 
            except VolunteeredFor.DoesNotExist:
                pitchedinPitches = None
                empty = True

            if pitchedinPitches != None:
                    paginator = Paginator(pitchedinPitches, 15) 
                    page = request.GET.get('page')
                    try:
                        pitchedin_page_pitches = paginator.page(page)
                    except PageNotAnInteger:
                        # If page is not an integer, deliver first page.
                        pitchedin_page_pitches  = paginator.page(1)
                    except EmptyPage:
                        # If page is out of range (e.g. 9999), deliver last page of results.
                        pitchedin_page_pitches  = paginator.page(paginator.num_pages)
            else:
                pitchedin_page_pitches  = None

            context=context_loggedin.copy()
            context.update({'user_pitches': pitchedin_page_pitches,
                        'my': False,
                        'empty': empty, 
                        'headval': "Pitched-in Pitches",
                        'display_pitch_url': reverse_lazy('display_pitch'),
                        'loggedin':loggedin,
                        'profile_url':profile_url})

            return render(request, 'pitch/mypitches.html', context)

        else:
            login_url = reverse_lazy('login')
            return redirect(login_url+"?red=pitchedin_pitch")        

def comment_pitch(request):
    if request.method == "GET":
        user = request.user
        comment = request.GET.get("comment","")
        try:
            pitch = Pitch.objects.get(id = request.GET.get('pitch_id'))
        except Pitch.DoesNotExist:
            return HttpResponse("Invalid pitch") 

        new_comment= Comment(user = user, pitch = pitch, comment=comment)
        new_comment.save()
        return HttpResponse("true")

def devteam_add(request):
    if request.method == "POST":
        devteamlist = request.POST.getlist("devteam")
        pitch = Pitch.objects.get(id = request.POST.get("pitch"))
        for devmember in devteamlist:
            user =  User.objects.get(username=devmember)       
            new_member = DevTeam(user = user, pitch  = pitch)
            new_member.save()
            VolunteeredFor.objects.get(pitch = pitch, user = user).delete() 

        return HttpResponse("true")

def add_comment(request):
    if request.method == "GET":
        user = request.user 
        pitch = Pitch.objects.get(id = request.GET.get('pitch'))
        comment = request.GET.get('comment')
        new_comment = Comment(user = user, pitch = pitch, comment = comment)
        new_comment.save()
        profile_url = reverse("profile", args = (user.id,))
        
        context = {'profile_url':profile_url, 'renderuser': user, 'my':True, 'user':user, 'comment':comment}
        return render(request, 'pitch/displaycomment.html', context)