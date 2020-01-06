from django.db import models


class Ingredient(models.Model):

    """ Cosmetic Ingredients Model Definition """

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    oily = models.CharField(max_length=1)
    dry = models.CharField(max_length=1)
    sensitive = models.CharField(max_length=1)


class Product(models.Model):

    """ Cosmectic Produdcts Model Definition """

    CATEGORY_SKIN = "skincare"
    CATEGORY_MASK = "maskpack"
    CATEGORY_SUN = "suncare"
    CATEGORY_BASE = "baskemakeup"

    CATEGORY_CHOICES = (
        (CATEGORY_SKIN, "Skin care"),
        (CATEGORY_MASK, "Mask pack"),
        (CATEGORY_SUN, "Sun care"),
        (CATEGORY_BASE, "Base makeup"),
    )

    id = models.IntegerField(primary_key=True)
    imageId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=11, default=CATEGORY_SKIN
    )
    ingredients = models.ManyToManyField("Ingredient", related_name="products",)
    monthlySales = models.IntegerField()

    def calculate_ingredient_score(self) -> int:
        pass
