from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request):

    template = loader.get_template('index.html')
    return render_to_response('index.html', context_instance=RequestContext(request))
