from django.core.management.base import BaseCommand, CommandError

from deezerdata.models import *
from musicdata.models import *
from platform_apis.models import *


class Command(BaseCommand):
    help = 'Clear database tables except Profile and LocationRecord'

    def handle(self, *args, **options):

        Genre.objects.all().delete()
        Market.objects.all().delete()
        ReleaseGroupContribution.objects.all().delete()
        RecordingContribution.objects.all().delete()
        DeezerTrack.objects.all().delete()
        Recording.objects.all().delete()
        DeezerAlbum.objects.all().delete()
        ReleaseGroup.objects.all().delete()
        Artist.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Success'))
