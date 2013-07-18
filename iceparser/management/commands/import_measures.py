from django.core.management import BaseCommand
from iceparser.models import Measure


class Command(BaseCommand):
    def handle(self, *args, **options):
        Measure.import_from_icecat()