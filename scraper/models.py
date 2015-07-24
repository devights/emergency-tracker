from django.db import models
from django.utils import timezone


class Incident(models.Model):
    incident_id = models.CharField(max_length=10, primary_key=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    location_text = models.CharField(max_length=255)
    type = models.ForeignKey('IncidentType')
    level = models.IntegerField(null=True)

    def create_incident(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
        self.save()

    def to_json(self):
        json = {'incident_id': self.incident_id,
                'start': self.start.isoformat(),
                'end': None,
                'location': self.location_text,
                'type': self.type.type_name,
                'level': self.level}
        if self.end is not None:
            json['end'] = self.end.isoformat()
        return json


class IncidentType(models.Model):
    incident_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=255)


class Dispatch(models.Model):
    vehicle_id = models.ForeignKey('Vehicle')
    incident_id = models.ForeignKey('Incident')
    timestamp = models.DateTimeField()

    def dispatch(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
        self.timestamp = timezone.now()
        self.save()


class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey('VehicleType')


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
