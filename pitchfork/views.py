from django.shortcuts import render, render_to_response
from users import models as user_models
from users import views as user_views
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import models as moder
from django.core.exceptions import *
from django.db import *
from django.contrib.auth.hashers import *
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pitch.models import *
from django.db.models import Model
import urllib
import datetime
from django.db.models.loading import cache as model_cache

def home(request): 
	if request.user.is_authenticated() and not request.user.is_superuser:
		loggedin = True
	else:
		loggedin = False

	context={'headval' : "",
			'loggedin' : loggedin,
            'pitch_url' : reverse_lazy('pitch'),
            'mypitches_url': reverse_lazy('user_pitch'),
            'otherpitches_url': reverse_lazy('other_pitch'),
            'logout_url':reverse_lazy('logout'),
            'login_url':reverse_lazy('login'),
            }
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
