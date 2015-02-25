from django.test import TestCase
from scraper.scraper import Scraper
from scraper.models import Incident, Vehicle, Dispatch
INCIDENTS =[{"status": "active", "incident_id": "F150020627", "level": 1, "datetime": "2/24/2015 8:42:24 PM", "location": "2717 Dexter Av N", "units": ["E9"], "type": "Medic Response"},
            {"status": "closed", "incident_id": "F150020627", "level": 1, "datetime": "2/24/2015 8:42:24 PM", "location": "2717 Dexter Av N", "units": ["E9"], "type": "Medic Response"},
            {"status": "active", "incident_id": "F150020626", "level": 1, "datetime": "2/24/2015 8:41:24 PM", "location": "5th Av / Pine St", "units": ["E9"], "type": "Aid Response"},
            {"status": "closed", "incident_id": "F150020624", "level": 1, "datetime": "2/24/2015 8:26:16 PM", "location": "S Spokane St / Beacon Av S", "units": ["E13"], "type": "MVI - Motor Vehicle Incident"},
            {"status": "closed", "incident_id": "F150020622", "level": 1, "datetime": "2/24/2015 8:10:19 PM", "location": "5983 Rainier Av S", "units": ["E28"], "type": "Aid Response"},
            {"status": "active", "incident_id": "F150020627", "level": 1, "datetime": "2/24/2015 8:04:32 PM", "location": "9616 37th Av Sw", "units": ["L11"], "type": "Activated CO Detector"},
            {"status": "active", "incident_id": "F150020610", "level": 1, "datetime": "2/24/2015 7:09:51 PM", "location": "6507 Ellis Av S", "units": ["CHAP5", "A1"], "type": "Aid Response"}]


class TestScraper(TestCase):
    def test_data(self):
        sc = Scraper()
        sc.store_data(INCIDENTS[0])
        self.assertEqual("F150020627", Incident.objects.get(id=1).incident_id)
        self.assertEqual("2717 Dexter Av N", Incident.objects.get(id=1).location_text)
        self.assertEqual("Medic Response", Incident.objects.get(id=1).type.type_name)
        self.assertEqual("E9", Vehicle.objects.get(id=1).name)

    def test_no_dupes(self):
        sc = Scraper()
        sc.store_data(INCIDENTS[0])
        self.assertEqual(1, len(Incident.objects.all()))
        sc.store_data(INCIDENTS[0])
        self.assertEqual(1, len(Incident.objects.all()))


    def test_open_close(self):
        sc = Scraper()
        sc.store_data(INCIDENTS[0])
        self.assertIsNone(Incident.objects.get(id=1).end)
        sc.store_data(INCIDENTS[1])
        self.assertIsNotNone(Incident.objects.get(id=1).end)

    def test_dupe_vehic(self):
        sc = Scraper()
        sc.store_data(INCIDENTS[0])
        self.assertEqual(1, len(Vehicle.objects.all()))
        sc.store_data(INCIDENTS[2])
        self.assertEqual(1, len(Vehicle.objects.all()))

    def test_multi_vehic(self):
        sc = Scraper()
        sc.store_data(INCIDENTS[6])
        self.assertEqual(2, len(Vehicle.objects.all()))

    def test_followup_dispatch(self):
        sc = Scraper()
        sc.store_data(INCIDENTS[5])
        self.assertEqual(1, len(Incident.objects.all()))
        self.assertEqual(1, len(Dispatch.objects.all()))
        sc.store_data(INCIDENTS[0])
        self.assertEqual(1, len(Incident.objects.all()))
        self.assertEqual(2, len(Dispatch.objects.all()))

    def test_closed(self):
        sc = Scraper()
        sc.store_data(INCIDENTS[1])
        self.assertEqual(0, len(Incident.objects.all()))