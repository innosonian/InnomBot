from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from vacations.models import VacationType


class Command(BaseCommand):
    help = 'init vacation type'

    def handle(self, *args, **options):
        categories = [
            ('연차/월차', 1),
            ('반차', 0.5),
        ]
        for name, weight in categories:
            if not VacationType.objects.filter(name=name).exists():
                VacationType.objects.create(name=name, weight=weight)
        self.stdout.write(self.style.SUCCESS("Init vacation type"))
