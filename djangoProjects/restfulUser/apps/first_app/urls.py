from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^users/(?P<number>\d+)$', views.show, name="show"),
  url(r'^users/(?P<number>\d+)/edit$', views.edit, name="update"),
  url(r'^users/new$', views.add, name="new"),
  url(r'^users/create$', views.create, name="create"),
  url(r'^users/(?P<number>\d+)/destroy$', views.destroy, name="destroy"),
  url(r'^GoBack$', views.GoBack, name=""),
  #url(r'users/(?P<number>\d+)$', views.show),
]