from django.conf.urls import patterns, url

from LDT import views

urlpatterns = patterns ('',
    url(r'^$', views.index),
)
