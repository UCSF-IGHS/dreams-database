from django.core.management.base import BaseCommand, CommandError
from DreamsApp.models import Client
from faker import Faker

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('client_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            fake = Faker()
            from django.conf import settings
            if settings.GENERATE_FAKE_DATA and settings.GENERATE_FAKE_DATA == True:
                clients = Client.objects.all()
                for c in clients:
                    self.stdout.write(self.style.SUCCESS('Client name before update {} {}'.format(c.first_name, c.last_name)))
                    c.first_name = fake.first_name_female()
                    c.last_name = fake.last_name()
                    c.middle_name = fake.first_name()
                    c.phone_number = fake.phone_number()[:12]
                    c.guardian_name = fake.name()
                    c.guardian_phone_number = fake.phone_number()[:12]
                    c.guardian_national_id = fake.phone_number()[:10]
                    c.save()
                    self.stdout.write(self.style.SUCCESS('Client name after update {} {} {}'.format(c.id, c.first_name, c.last_name)))
                self.stdout.write(self.style.SUCCESS('Successfully updated the client with fake name'))
            else:
                self.stdout.write(self.style.SUCCESS('Successfully ran command but client name not updated as GENERATE_FAKE_DATA setting must be True'))


        except Client.DoesNotExist:
            raise CommandError('No clients exist')
        