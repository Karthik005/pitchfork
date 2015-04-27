from django.conf.urls import patterns, url

from pitch import views

urlpatterns = patterns('',
    url(r'^$', views.pitch_view, name='pitch'),
    url(r'^pitch_validate$', views.pitch_validate, name='pitch_validate'),
    url(r'^mypitches/$', views.user_pitch, name='user_pitch'),
)

    # '''
    # url(r'^login/login_validate$', views.login_validate, name='login_validate'),
    # url(r'^register/$', views.register_view, name='register'),
    # url(r'^register/register_validate$', views.register_validate, name='register_validate'),
    # url(r'^register/register_user$', views.register_user, name='register_user'),
    # url(r'^logout$', views.logout_view, name='logout'),
    # '''