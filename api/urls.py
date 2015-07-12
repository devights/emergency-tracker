from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.views.engine_search import EngineSearch

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^v1/search', EngineSearch().run),
)
