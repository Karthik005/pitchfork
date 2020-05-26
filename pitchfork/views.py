from django.shortcuts import render
from users import models as user_models
from users import views as user_views
from pitch import models as pitch_models
from pitch import views as pitch_views
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import models as moder
from django.core.exceptions import *
from django.db import *
from django.contrib.auth.hashers import *
from django.urls import reverse, reverse_lazy
from pitch.models import *
from django.db.models import Model
import urllib
import datetime

context_init = {
                'pitch_url' : reverse_lazy('pitch'),
                'mypitches_url': reverse_lazy('user_pitch'),
                'otherpitches_url': reverse_lazy('other_pitch'),
                'pitchedinpitches_url': reverse_lazy('pitchedin_pitch'),
                'logout_url':reverse_lazy('logout'),
                'login_url':reverse_lazy('login'),
                'register_url':reverse_lazy('register'),
                }
def home(request): 
    if request.user.is_authenticated() and not request.user.is_superuser:
        loggedin = True
        profile_url=reverse('profile', args = (request.user.id,))
    else:
        loggedin = False
        profile_url = None

    context = context_init.copy()
    context.update({'headval' : "Index",
            'loggedin' : loggedin,
            'profile_url':profile_url,
            })
    return render(request, 'main/home.html', context)

def request_redirect(request):
    red = request.GET.get('red')
    if red[0] != '/':
        if red == None or red == "null" or red == "undefined":
            red_url = reverse_lazy('home')
            
        else:
            red_url = reverse(red)

        return redirect(red_url)
    
    else:
        return redirect(red)
