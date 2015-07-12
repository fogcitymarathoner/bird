from django.conf.urls import patterns, include, url
from django.contrib import admin
from tpages.views import add
from tpages.views import list
from tpages.views import edit
from tpages.views import delete
from tpages.views import toolkit
from tpages.views import ninetymoredays
from tpages.views import show

urlpatterns = patterns('',
    url(r'^add', add, name='add'),
    url(r'^$', list, name='list'),
    url(r'^edit/(?P<token>[0-9a-fA-F]+)', edit, name='edit'),
    url(r'^delete/(?P<token>[0-9a-fA-F]+)', delete, name='delete'),
    url(r'^toolkit/(?P<token>[0-9a-fA-F]+)', toolkit, name='toolkit'),
    url(r'^ninetymoredays/(?P<token>[0-9a-fA-F]+)', ninetymoredays, name='ninetymoredays'),
    url(r'^(?P<token>[0-9a-fA-F]+)',show, name='show'),
)
