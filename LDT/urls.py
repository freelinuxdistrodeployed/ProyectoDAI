from django.conf.urls import patterns, url

from LDT import views

urlpatterns = patterns ('',
    url(r'^$', views.index),
    #url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    #url(r'^index/$', views.index),
)
