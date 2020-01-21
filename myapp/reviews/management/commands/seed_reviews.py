import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from myapp.users import models as user_models
from myapp.products import models as product_models
from myapp.reviews import models as review_models


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
        number = options.get("number")
        seeder = Seed.seeder()

        users = user_models.User.objects.all()
        products = product_models.Product.objects.all()

        seeder.add_entity(
            review_models.Review,
            number,
            {
                "score": lambda x: random.randint(0, 5),
                "user": lambda x: random.choice(users),
                "product": lambda x: random.choice(products),
            },
        )

        created_reviews = seeder.execute()
        created_clean = flatten(list(created_reviews.values()))

        # many to many fields
        favorite_users = list(user_models.User.objects.all())

        for review_id in created_clean:
            review = review_models.Review.objects.get(id=review_id)
            favorite_max = random.randint(0, len(favorite_users) // 2)
            selected_users = random.sample(favorite_users, favorite_max)
            for user in selected_users:
                review.favorite_users.add(user)

        self.stdout.write(self.style.SUCCESS(f"{number} Reviews created"))
