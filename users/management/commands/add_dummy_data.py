import requests
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'populates DB with dummy values'
    URL = 'https://datapeace-storage.s3-us-west-2.amazonaws.com/dummy_data/users.json'

    def handle(self, *args, **options):
        r = requests.get(self.URL)
        users = [User(**u) for u in r.json()]

        User.objects.bulk_create(users)

        msg = 'Adding {} users.'.format(User.objects.all().count())
        self.stdout.write(self.style.SUCCESS(msg))
