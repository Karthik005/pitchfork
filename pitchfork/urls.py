from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    
    url(r'^$', 'pitchfork.views.home', name='home'),
    
    url(r'^users/', include('users.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
