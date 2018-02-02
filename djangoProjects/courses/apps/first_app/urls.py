from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index),
  url(r'^courses/create$', views.create, name="create"),
  url(r'^courses/(?P<number>\d+)/confirm$', views.confirm, name="confirm"),
  url(r'^courses/(?P<number>\d+)/destroy$', views.destroy, name="destroy"),
]