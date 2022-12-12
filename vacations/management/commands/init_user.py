from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from vacations.models import User


class Command(BaseCommand):
    help = 'init setting food category'

    def handle(self, *args, **options):
        categories = [
            ('U02QA8EFY8Y', 'Sofi'),
            ('U04ARD6H3PU', 'Ria'),
            ('U03D904UB9D', 'Cecilia'),
            ('U038F94ADGS', 'Clarissa'),
            ('ULUDN93MZ', 'Erick'),
            ('U0MF8CBF1', 'Harry'),
            ('UNWJE78LC', 'Hayden'),
            ('UR3B7NSRW', 'Kevin'),
            ('U03HZ7B5YCR', 'ellie'),
            ('U01VAA61WAZ', 'Scarlet'),
            ('U0MM2MRCP', 'Jason'),
            ('U0Q7L1UDR', 'Nancy'),
            ('U03JHTCC0KV', 'Mina'),
            ('U02NFN3FZ42', 'Sergio'),
            ('U03SEUB9VMM', 'Mark'),
            ('U0MFD1Y1X', 'Moley'),
        ]
        for user_id, name in categories:
            try:
                User.objects.get(id=user_id)
            except ObjectDoesNotExist:
                User.objects.create(id=user_id, name=name)
        self.stdout.write(self.style.SUCCESS("Init user info"))