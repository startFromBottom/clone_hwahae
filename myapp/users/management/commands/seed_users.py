import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from myapp.users.models import User
from myapp.products.models import Product, Ingredient


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
            User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
                "point": random.randint(1, 5),
                "email_verified": True,
            },
        )
        created_users = seeder.execute()
        created_clean = flatten(list(created_users.values()))

        # many to many fields
        favs_products = list(Product.objects.all())
        favs_ingredients = list(Ingredient.objects.all())

        for id in created_clean:
            user = User.objects.get(id=id)

            product_max = random.randint(1, 20)
            selected_products = random.sample(favs_products, product_max)

            ingredient_max = random.randint(1, 15)
            selected_ingredients = random.sample(favs_ingredients, ingredient_max)

            for product in selected_products:
                user.favs_products.add(product)

            for ingredient in selected_ingredients:
                user.favs_ingredients.add(ingredient)

        self.stdout.write(self.style.SUCCESS("User created"))
