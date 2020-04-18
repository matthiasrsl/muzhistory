from django.core.management.base import BaseCommand, CommandError
from deezerdata.models.deezer_account import *

class Command(BaseCommand):
    help = 'Updates the Deezer listening history of every DeezerAccount.'


    def handle(self, *args, **options):

        all_deezer_accounts = DeezerAccount.objects.all()
        for account in all_deezer_accounts:
            account.retrieve_history()

        self.stdout.write(self.style.SUCCESS('Success'))