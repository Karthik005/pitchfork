from django.conf.urls import include, url
from django.contrib import admin
import pitchfork.views as views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^redirect/$', views.request_redirect, name='redirect'),

    url(r'^users/', include('users.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^pitch/', include('pitch.urls')),

]
