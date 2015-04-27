from django.shortcuts import render
from django.http import HttpResponse


def home(request): 
	if request.user.is_authenticated() and not request.user.is_superuser:
		loggedin = True
	else:
		loggedin = False

	context={'headval' : "",
			'loggedin' : loggedin}
	return render(request, 'main/home.html', context)
