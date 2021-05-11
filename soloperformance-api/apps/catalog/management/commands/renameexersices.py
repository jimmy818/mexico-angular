
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpRequest
from apps.catalog import utils
                                                                                
class Command(BaseCommand):
    help = 'Add exercises'

    def handle(self, *args, **options):
        request = HttpRequest()
        utils.rename_exersice()
        self.stdout.write(self.style.SUCCESS('Successfully.....'))