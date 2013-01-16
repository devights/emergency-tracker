from django.db import models


class Incident(models.Model):
    incident_id = models.AutoField(primary_key=True)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)
    location_text = models.CharField(max_length=255)
    type_id = models.ForeignKey('IncidentType')
    level = models.IntegerField()

class IncidentType(models.Model):
    incident_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=255)
