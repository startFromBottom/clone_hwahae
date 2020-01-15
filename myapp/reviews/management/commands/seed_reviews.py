import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from myapp.users.models import User
from myapp.products.models import Product
from myapp.reviews.models import Review


class Command(BaseCommand):

    help = "This command create fake reviews"

    def add_arguments(self, parsor):

        parsor.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many reviews do you want to create",
        )

    def handle(self, *args, **options):
        pass
