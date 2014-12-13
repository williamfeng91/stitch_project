from django.conf.urls import patterns, include, url
from trello import views

urlpatterns = patterns('',
    url(r'^request/$', views.request_handler),
    url(r'^Members/new_member/$', views.new_member),
    url(r'^Members/$', views.members),
    url(r'^Members/(\d+)/$', views.member),
    url(r'^new_board/$', views.new_board),
    url(r'^Boards/(\d+)/$', views.board),
    url(r'^Boards/(\d+)/new_list/$', views.new_list),
    url(r'^Boards/(\d+)/Lists/(\d+)/$', views.list),
    url(r'^Boards/(\d+)/Lists/(\d+)/new_card/$', views.new_card),
    url(r'^Boards/(\d+)/Lists/(\d+)/Cards/(\d+)/$', views.card),
    url(r'^Boards/(\d+)/Lists/(\d+)/Cards/(\d+)/new_label/$', views.new_label),
    url(r'^.*$', views.home),
)
