from django.conf.urls import patterns, url

from pitch import views

urlpatterns = patterns('',
    url(r'^$', views.pitch_view, name='pitch'),
    url(r'^pitch_validate$', views.pitch_validate, name='pitch_validate'),
    url(r'^vote/$', views.vote_pitch, name='vote_pitch'),
    url(r'^remove/$', views.remove_pitch, name='remove_pitch'),
    url(r'^pitchin/$', views.pitch_in, name='pitch_in'),
    url(r'^mypitches/$', views.user_pitch, name='user_pitch'),
    url(r'^otherpitches/$', views.other_pitch, name='other_pitch'),
    url(r'^pitchedinpitches/$', views.pitchedin_pitch, name='pitchedin_pitch'),
    url(r'^devteamadd/$', views.devteam_add, name='devteam_add'),
    url(r'^addcomment/$', views.add_comment, name='add_comment'),

    url(r'^display_pitch/(?P<pitch_id>(.)*)/', views.display_pitch, name='display_pitch'),
# (\w+)
)

    # '''
    # url(r'^login/login_validate$', views.login_validate, name='login_validate'),
    # url(r'^register/$', views.register_view, name='register'),
    # url(r'^register/register_validate$', views.register_validate, name='register_validate'),
    # url(r'^register/register_user$', views.register_user, name='register_user'),
    # url(r'^logout$', views.logout_view, name='logout'),
    # '''