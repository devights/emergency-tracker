from django.core.management.base import BaseCommand
from scraper.models import Incident, IncidentType, \
    Dispatch, Vehicle, VehicleType
import csv
import datetime
import re
from pytz import timezone

import time


class Command(BaseCommand):
    help = 'Imports data from legacy database csv'

    def add_arguments(self, parser):
        parser.add_argument('incident_file', help="incident csv file")
        parser.add_argument('dispatch_file', help="dispatch csv file")

    incident_type_map = {}
    vehicle_map = {}
    vehicle_type_map = {}

    def handle(self, *args, **options):
        dispatch_path = options['dispatch_file']
        incident_path = options['incident_file']

        incident_models = []

        start = time.time()
        with open(incident_path, 'rb') as csvfile:
            incident_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            count = 0
            for row in incident_reader:
                try:
                    incident_models.append(self._process_incident(row))
                except Exception as ex:
                    print ex
                    print row
                    pass
                count += 1
                if count % 10000 == 0:
                    Incident.objects.bulk_create(incident_models)
                    incident_models = []
            Incident.objects.bulk_create(incident_models)

        dispatch_models = []
        with open(dispatch_path, 'rb') as csvfile:
            dispatch_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            count = 0
            for row in dispatch_reader:
                try:
                    dispatch_models.append(self._process_dispatch(row))
                except Exception as ex:
                    print ex
                    print row
                    pass
                count += 1
                if count % 10000 == 0:
                    Dispatch.objects.bulk_create(dispatch_models)
                    dispatch_models = []
            Dispatch.objects.bulk_create(dispatch_models)
        print time.time() - start

    def _process_incident(self, row):
        date_format = '%Y-%m-%d %H:%M:%S'
        local_tz = timezone('America/Los_Angeles')
        inc = Incident()
        inc.incident_id = row[0]
        inc.start = local_tz.localize(datetime.datetime.strptime(
            row[1], date_format))
        try:
            inc.end = local_tz.localize(datetime.datetime.strptime(
                row[2], date_format))
        except Exception:
            pass
        inc.location_text = row[3]

        type_name = row[4]
        if type_name in self.incident_type_map:
            inc.type = self.incident_type_map[type_name]
        else:
            incident_type, created = IncidentType.objects.get_or_create(
                type_name=type_name)
            inc.type = incident_type
            self.incident_type_map[type_name] = incident_type
        inc.level = row[5]
        return inc

    def _process_dispatch(self, row):
        date_format = '%Y-%m-%d %H:%M:%S'
        local_tz = timezone('America/Los_Angeles')
        dispatch = Dispatch()
        dispatch.incident_id = Incident.objects.get(incident_id=row[1])
        dispatch.timestamp = local_tz.localize(
            datetime.datetime.strptime(row[2], date_format)
        )

        p = re.compile("([A-Za-z]+)")
        match = p.search(row[0])
        try:
            vehicle_type_string = match.group()
        except AttributeError:
            vehicle_type_string = "UNKNOWN"

        if vehicle_type_string in self.vehicle_type_map:
            vehic_type = self.vehicle_type_map[vehicle_type_string]
        else:
            vehic_type, created = VehicleType.objects.get_or_create(
                name=vehicle_type_string)
            self.vehicle_type_map[vehicle_type_string] = vehic_type

        vehic_name = row[0]
        if vehic_name in self.vehicle_map:
            vehicle = self.vehicle_map[vehic_name]
        else:
            vehicle, created = \
                Vehicle.objects.get_or_create(name=vehic_name, type=vehic_type)
            self.vehicle_map[vehic_name] = vehicle

        dispatch.vehicle_id = vehicle
        return dispatch
