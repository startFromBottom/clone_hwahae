from django.core.management.base import BaseCommand
from myapp.users.models import User


class Command(BaseCommand):

    help = "This command creates superuser"

    def handle(self, *args, **options):

        admin = User.objects.get_or_none(username="ebadmin")

        if admin is None:
            User.objects.create_superuser("ebadmin", "aaa@gmail.com", "programmers")
            self.stdout.write(self.style.SUCCESS("Superuser Created!"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser Exists!"))
