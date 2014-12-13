from django.conf.urls import patterns, include, url
from trello import views

urlpatterns = patterns('',
    url(r'^request/$', views.request_handler),
    url(r'^new_board/$', views.new_board),
    url(r'^Boards/(\d+)/new_list/$', views.new_list),
    url(r'^Boards/(\d+)/$', views.board),
    url(r'^Boards/(\d+)/Lists/(\d+)/$', views.list),
    url(r'^.*$', views.home),
)
