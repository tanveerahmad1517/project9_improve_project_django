from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.menu_list, name='list'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.menu_create_edit, name='edit'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='detail'),
    url(r'^menu/item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    url(r'^menu/new/$', views.menu_create_edit, name='new'),
]
