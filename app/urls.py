from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse

from app import rest_views
from . import views

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^$', views.landing, name='landing'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^userprofile/$', views.UserProfile.as_view(), name='userprofile'),
    # url(r'^userprofile/$', views.updateInfo, name='updateInfo'),
    url(r'^ajax/updatelocation/$', views.updatelocat, name='updatelocation'),
    url(r'^ajax/listFriend/$', views.listV.as_view(), name='list'),
]
