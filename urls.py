__author__ = 'tbartel'
from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^module/(?P<module_name>[\w-]+)/$', module_overview),
    url(r'^module/all/graph/$', all_module_graph),
    url(r'^module/(?P<module_name>[\w-]+)/graph/$', module_graph),
    url(r'^instance/(?P<instance_name>[\w-]+)/$', instance_overview),
]