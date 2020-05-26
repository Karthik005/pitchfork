from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^login/login_validate$', views.login_validate, name='login_validate'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^register/register_validate$', views.register_validate, name='register_validate'),
    url(r'^register/register_user$', views.register_user, name='register_user'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^login/?', views.login_view, name='login'),
    url(r'^profile/(?P<user_id>([0-9])*)/', views.view_profile, name='profile'),
    #url(r'^login?red=([a-z]*)$', views.login_view, name='login'),
]