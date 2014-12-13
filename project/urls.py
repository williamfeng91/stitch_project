from django.conf.urls import patterns, include, url
from trello import views

urlpatterns = patterns('',
    url(r'^Boards/(\d+)$', views.display_board),
    url(r'^.*$', views.display_overview),
)
