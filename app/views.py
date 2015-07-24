from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from scraper.models import Incident, Dispatch, Vehicle, VehicleType
from django.db.models import Count
from app.utilities import get_vehicle_type_details


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

def vehicles(request):
    vehicles = VehicleType.objects.annotate(type_count=Count('vehicle')).order_by('-type_count')
    print len(Vehicle.objects.all())
    print len(VehicleType.objects.all())
    print len(vehicles)
    vehicles = get_vehicle_type_details(vehicles)

    context = RequestContext(request, {
        'types': vehicles
    })
    return render_to_response('vehicles.html',
                              context_instance=context)