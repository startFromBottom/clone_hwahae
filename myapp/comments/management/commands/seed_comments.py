import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from myapp.users import models as user_models
from myapp.reviews import models as review_models
from myapp.comments import models as comment_models


class Command(BaseCommand):

    help = "This command create fake reviews"

    def add_arguments(self, parsor):

        parsor.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many comments do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()

        users = user_models.User.objects.all()
        reviews = review_models.Review.objects.all()

        seeder.add_entity(
            comment_models.Comment,
            number,
            {
                "comment_user": lambda x: random.choice(users),
                "review": lambda x: random.choice(reviews),
            },
        )

        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Comments created"))
