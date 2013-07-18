from django.core.management import BaseCommand
from iceparser.models import Language


class Command(BaseCommand):
    def handle(self, *args, **options):
        Language.import_from_icecat()