from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^$', views.index),
  url(r'^register/$', views.register),
  url(r'^login/$', views.login),
  url(r'^books/$', views.result),
  url(r'^books/add$', views.add),
  url(r'^addBook$', views.addBook),
  url(r'^goback$', views.goback),
  url(r'^addReview/$', views.addReview),
  url(r'^books/(?P<number>\d+)$', views.bookReviews),
  url(r'^user/(?P<number>\d+)$', views.user),
  url(r'^destroyComment/$', views.destroyComment),
  

 # url(r'^users/(?P<number>\d+)$', views.show, name="show"),
 # url(r'^users/(?P<number>\d+)/edit$', views.edit, name="update"),
 # url(r'^users/new$', views.add, name="new"),
 # url(r'^users/create$', views.create, name="create"),
 # url(r'^users/(?P<number>\d+)/destroy$', views.destroy, name="destroy"),
 # url(r'^GoBack$', views.GoBack, name=""),
  #url(r'users/(?P<number>\d+)$', views.show),
]