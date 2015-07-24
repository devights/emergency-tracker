from django.conf.urls import patterns, include, url
from app.views import index

urlpatterns = patterns('',
                       url(r'.*', index, name="home"),
                       )
