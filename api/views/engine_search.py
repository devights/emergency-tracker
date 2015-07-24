from api.views.rest_dispatch import RESTDispatch
from django.http import HttpResponse
import json
from scraper.models import Vehicle, Dispatch, Incident


class EngineSearch(RESTDispatch):
    """
    Returns incidents for a given vehicle, optional paramater to specify count
    """

    def GET(self, request, engine_name):
        incident_count = request.GET.get('count')
        if not incident_count:
            incident_count = 1

        try:
            vehicle = Vehicle.objects.get(name=engine_name)
        except Vehicle.DoesNotExist:
            return self.invalid_vehicle(engine_name)

        try:
            dispatches = Dispatch.objects.filter(
                vehicle_id=vehicle
            ).order_by('-timestamp')[:incident_count].values(
                'incident_id__incident_id')
        except Dispatch.DoesNotExist:
            return HttpResponse(json.dumps([]))

        try:
            incidents = Incident.objects.filter(incident_id__in=dispatches)
        except Incident.DoesNotExist:
            return HttpResponse(json.dumps([]))
        incident_json = []
        for incident in incidents:
            incident_json.append(incident.to_json())

        return HttpResponse(json.dumps({'incidents': incident_json,
                                        'count': len(incident_json)}))

    def invalid_vehicle(self, name):
        return HttpResponse('Invalid Vehicle Name %s' % str(name))
