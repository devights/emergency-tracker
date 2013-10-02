from django.db import models


class Incident(models.Model):
    incident_id = models.CharField(max_length=10)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)
    location_text = models.CharField(max_length=255)
    type = models.ForeignKey('IncidentType')
    level = models.IntegerField()

class IncidentType(models.Model):
    incident_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=255)
    
class Dispatch(models.Model):
    vehicle_id = models.ForeignKey('Vehicle')
    incident_id = models.ForeignKey('Incident') 
    timestamp = models.DateTimeField(auto_now_add=True)

class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey('VehicleType')

class VehicleType(models.Model):
    name = models.CharField(max_length=32)