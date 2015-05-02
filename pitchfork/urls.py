from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    # Examples:
    
    url(r'^$', views.home, name='home'),
    url(r'^redirect/$', views.request_redirect, name='redirect'),

    url(r'^users/', include('users.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pitch/', include('pitch.urls')),

)
