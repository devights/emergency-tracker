import urllib2
import re
import logging
from django.core.exceptions import ObjectDoesNotExist
from lxml import etree
from StringIO import StringIO
from models import Vehicle, VehicleType, Incident, IncidentType, Dispatch
from django.utils import timezone

PAGE_URL = ('http://www2.cityofseattle.net/fire/realTime911/'
            'getRecsForDatePub.asp?action=Today&incDate=&rad1=des')


class Scraper:
    dispatch_logger = logging.getLogger('dispatch')
    incident_logger = logging.getLogger('incident')

    def fetch_data(self):
        response = urllib2.urlopen(PAGE_URL)
        html = response.read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html), parser)

        table = tree.xpath("//table[@bgcolor='#FFFFFF' and @cellpadding='2']")
        rows = table[0].getchildren()

        for row in rows:
            children = row.getchildren()
            incident = {}
            incident['datetime'] = children[0].text
            incident['incident_id'] = children[1].text
            incident['level'] = children[2].text
            incident['units'] = children[3].text.split(' ')
            incident['location'] = children[4].text
            incident['type'] = children[5].text
            incident['status'] = children[0].get('class')
            self.store_data(incident)

    def store_data(self, incident_data):
        incident_type, created = IncidentType.objects.get_or_create(
            type_name=incident_data['type'])
        incident = None
        try:
            incident = Incident.objects.get(
                incident_id=incident_data['incident_id'])
        except Incident.DoesNotExist:
            if incident_data['status'] == 'active':
                incident_args = {'incident_id': incident_data['incident_id'],
                                 'type': incident_type,
                                 'location_text': incident_data['location'],
                                 'level': incident_data['level']
                                 }
                incident = Incident()
                incident.create_incident(**incident_args)

                self.incident_logger.info("start, id: %s, type_id:"
                                          "\"%s\", loc_str: %s, lvl: %s"
                                          % (incident.incident_id,
                                             incident.type.type_name,
                                             incident.location_text,
                                             incident.level))

        if incident is not None and incident_data['status'] == 'closed' and \
                incident.end is None:
            incident.end = timezone.now()
            incident.save()
            self.incident_logger.info("end, id: %s" % incident.incident_id)

        for vehic_data in incident_data['units']:
            p = re.compile("([A-Za-z]+)")
            match = p.search(vehic_data)
            type_string = match.group()
            vehic_type, created = VehicleType.objects.get_or_create(
                name=type_string)

            vehicle, created = \
                Vehicle.objects.get_or_create(name=vehic_data,
                                              defaults={'type': vehic_type})
            if incident is not None:
                try:
                    Dispatch.objects.get(vehicle_id=vehicle,
                                         incident_id=incident)
                except ObjectDoesNotExist:
                    dispatch = Dispatch()
                    dispatch.dispatch(vehicle_id=vehicle,
                                      incident_id=incident)
                    self.dispatch_logger.info("vehic: %s, incident: %s" %
                                              (vehicle.name,
                                               incident.incident_id))
                    pass
