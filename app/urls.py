from django.conf.urls import patterns, include, url
from app.views import index, vehicles

urlpatterns = patterns('',
                       url(r'vehicles', vehicles, name="vehicles"),
                       url(r'.*', index, name="home")
                       )
