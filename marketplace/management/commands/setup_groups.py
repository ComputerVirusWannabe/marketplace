from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates regular and moderator user groups'

    def handle(self, *args, **kwargs):
        # Create regular group
        regular, created = Group.objects.get_or_create(name='regular')
        if created:
            self.stdout.write(self.style.SUCCESS('Created "regular" group'))
        else:
            self.stdout.write(self.style.WARNING('regular group already exists'))

        # Create moderator group
        moderator, created = Group.objects.get_or_create(name='moderator')
        if created:
            self.stdout.write(self.style.SUCCESS('Created "moderator" group'))
        else:
            self.stdout.write(self.style.WARNING('moderator" group already exists'))

        self.stdout.write(self.style.SUCCESS('\nGroups setup complete!'))