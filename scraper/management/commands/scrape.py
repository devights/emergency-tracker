from django.core.management.base import BaseCommand, CommandError
from scraper.scraper import Scraper


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        scraper = Scraper()
        scraper.fetch_data()
