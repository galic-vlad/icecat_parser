from django.core.management import BaseCommand
from iceparser.models import Feature


class Command(BaseCommand):
    def handle(self, *args, **options):
        Feature.import_from_icecat()