from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
    url(r'^login/$', views.login, name='login'),
    url(r'^login/login_validate$', views.login_validate, name='login_validate'),
)