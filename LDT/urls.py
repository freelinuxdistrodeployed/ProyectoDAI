from django.conf.urls import patterns, url

from LDT import views

urlpatterns = patterns ('',
    url(r'^$', views.login),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    #url(r'^index/$', views.index),
)
