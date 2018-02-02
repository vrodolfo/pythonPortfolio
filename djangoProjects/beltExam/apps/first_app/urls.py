from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index),
  url(r'^main/$', views.main),
  url(r'^register/$', views.register),
  url(r'^login/$', views.login),
  url(r'^travels/$', views.result),
  url(r'^addTrip/$', views.addTrip),
  #url(r'^add/(?P<number>\d+)$', views.add),
  url(r'^join/(?P<number>\d+)$', views.join),
  url(r'^add/$', views.add),
  url(r'^goback$', views.goback),
  url(r'^travels/destination/(?P<number>\d+)$', views.destination),

  
]