from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from scraper.models import Incident, Dispatch, Vehicle


def index(request):
    active_incidents = Incident.objects.exclude(end__isnull=False).order_by('-start')[:10]
    dispatches = Dispatch.objects.filter(incident_id__in=active_incidents)
    dispatched_vehicles = dispatches.values_list('vehicle_id').distinct()
    vehicles = Vehicle.objects.filter(id__in=dispatched_vehicles)

    context = RequestContext(request,
                             {'incidents': active_incidents,
                              'dispatches': dispatches,
                              'dispatched_vehicles': vehicles})
    return render_to_response('index.html',
                              context_instance=context)
