from django.core.management.base import BaseCommand, CommandError
from read_only_site.models import Player, Match

class Command(BaseCommand):
    help = 'Launches the discord bot'

    def handle(self, *args, **options):
        print('It works!')
