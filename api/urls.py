from django.conf.urls import patterns, include, url
from api.views.engine_search import EngineSearch

urlpatterns = patterns('',
                       url(r'^v1/enginesearch/(?P<engine_name>[A-Z0-9]+)',
                           EngineSearch().run),
                       )
