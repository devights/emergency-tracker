import urllib2
import re
from datetime import datetime
from lxml import etree
from StringIO import StringIO
from models import Vehicle, VehicleType, Incident, IncidentType, Dispatch

class Scraper:
    
    def fetch_data(self):
        url = "http://www2.cityofseattle.net/fire/realTime911/getRecsForDatePub.asp?action=Today&incDate=&rad1=des"
#        response = urllib2.urlopen(url)
        response = open('/home/devights/devel/emergency-tracker/fire.html', 'r')
        html = response.read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(html), parser)

        table = tree.xpath("//table[@bgcolor='#FFFFFF' and @cellpadding='2']/tbody")
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
        incident_type, created = IncidentType.objects.get_or_create(type_name=incident_data['type'])
        incident = None
        try:
            incident = Incident.objects.get(incident_id=incident_data['incident_id'])
        except Incident.DoesNotExist:
            if incident_data['status'] == 'active': 
                incident = Incident()
                incident.incident_id = incident_data['incident_id']
                incident.type = incident_type
                incident.location_text = incident_data['location']
                incident.level = incident_data['level']
                incident.save()
            
            #write incident text to splunk, include vehicles
        if incident is not None and incident_data['status'] == 'closed' and incident.end is None:
            print "ENDING AN EVENT"
            incident.end = datetime.now()
            print "end"
            incident.save()
            print "saved"
            
        for vehic_data in incident_data['units']:
            p = re.compile("([A-Za-z]+)")
            match = p.search(vehic_data)
            type_string = match.group()
            vehic_type, created = VehicleType.objects.get_or_create(name=type_string)
            
            vehicle, created = Vehicle.objects.get_or_create(name=vehic_data,
                                                            defaults={'type': vehic_type})
#            if created:
#                vehicle.type = vehic_type
#                vehicle.save
            
        #Store IncidentType
        #store incident
            #if closed, mark closed 
            #if open see if 
        
        
        
        
        