import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from myapp.users import models as user_models
from myapp.products import models as product_models
from myapp.reviews import models as review_models


class Command(BaseCommand):

    help = "This command create fake Users"

    def add_arguments(self, parsor):

        parsor.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many users do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            user_models.User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
                "point": lambda x: random.randint(1, 5),
                "email_verified": True,
            },
        )
        created_users = seeder.execute()
        created_clean = flatten(list(created_users.values()))

        # many to many fields
        favs_products = list(product_models.Product.objects.all())
        favs_ingredients = list(product_models.Ingredient.objects.all())
        scrap_reviews = list(review_models.Review.objects.all())

        for user_id in created_clean:
            user = user_models.User.objects.get(id=user_id)

            product_max = random.randint(1, 20)
            selected_products = random.sample(favs_products, product_max)

            for product in selected_products:
                user.favs_products.add(product)

            ingredient_max = random.randint(1, 15)
            selected_ingredients = random.sample(favs_ingredients, ingredient_max)

            for ingredient in selected_ingredients:
                user.favs_ingredients.add(ingredient)

            try:
                scrap_max = random.randint(1, 5)
                selected_reviews = random.sample(scrap_reviews, scrap_max)
            except ValueError:  # Sample larger than population or is negative
                continue

            for review in selected_reviews:
                user.scrap_reviews.add(review)

        self.stdout.write(self.style.SUCCESS(f"{number} User created"))
