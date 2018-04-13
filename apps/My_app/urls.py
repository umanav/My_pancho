from django.conf.urls import url
from . import views          
urlpatterns = [
    url(r'^$', views.index),
    url(r'^home$', views.home),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^create$', views.create),
    url(r'^add/(?P<id>\d+)$', views.add_item),
    url(r'^remove/(?P<id>\d+)$', views.remove_item),
    url(r'^delete/(?P<id>\d+)$', views.delete_item),
    url(r'^product/(?P<id>\d+)$', views.display_product),
]
