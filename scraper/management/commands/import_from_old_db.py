from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import MySQLdb
import MySQLdb.cursors
import csv


class Command(BaseCommand):
    help = 'Imports data from legacy database format'

    def handle(self, *args, **options):
        db = MySQLdb.connect(host= settings.OLD_DB_HOST,
                             user=settings.OLD_DB_USER,
                             passwd=settings.OLD_DB_PASS,
                             db=settings.OLD_DB_DB,
                             cursorclass=MySQLdb.cursors.SSCursor)

        cur = db.cursor()

        # Fetch and denormalize incidents then write to csv
        cur.execute("SELECT Incident.id, Incident.start, Incident.end, "
                    "Incident.location, IncidentType.name, Incident.level "
                    "from Incident left join IncidentType on "
                    "Incident.type_id=IncidentType.id")
        counter = 0
        with open('data_export_incident.csv', 'wb') as csvfile:
            incident_writer = csv.writer(csvfile, delimiter=',', quotechar='|',
                                         quoting=csv.QUOTE_MINIMAL)
            for row in cur:
                counter += 1
                if counter % 100000 == 0:
                    print "I: %i" % counter
                incident_writer.writerow([row[0], row[1], row[2], row[3],
                                          row[4], row[5]])

        # Fetch and denormalize dispatches then write to csv
        cur.execute("SELECT * from Dispatch")
        counter = 0
        with open('data_export_dispatch.csv', 'wb') as csvfile:
            dispatch_writer = csv.writer(csvfile, delimiter=',', quotechar='|',
                                         quoting=csv.QUOTE_MINIMAL)
            for row in cur:
                counter += 1
                if counter % 100000 == 0:
                    print "D: %i" % counter
                dispatch_writer.writerow([row[0], row[1], row[2]])