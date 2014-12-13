from django.conf.urls import patterns, include, url
from trello import views

urlpatterns = patterns('',
    url(r'^new_board$', views.new_board),
    url(r'^request$', views.request_handler),
    url(r'^Boards/(\d+)$', views.board),
    url(r'^.*$', views.home),
)
