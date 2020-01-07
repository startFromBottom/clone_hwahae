from django.db import models


class Ingredient(models.Model):

    """ Cosmetic Ingredients Model Definition """

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    oily = models.CharField(max_length=1)
    dry = models.CharField(max_length=1)
    sensitive = models.CharField(max_length=1)

    def ingredient_score(self):
        """ 
        calculate ingredient score by using oily, dry, sensitive columns
        based on the following criteria
        
        < criteria >
        "O" -> +1
        " " -> +0
        "-" -> -1

        """
        score = 0
        for each in (self.oily, self.dry, self.sensitive):
            if each == "O":
                score += 1
            elif each == "X":
                score -= 1
        return score

    def __str__(self):
        return self.name


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

    def product_score(self):
        """
        calculate ingredient score of product
        by adding each score of ingredient
        """
        score = 0
        for ingredient in self.ingredients.all():
            score += ingredient.ingredient_score()
        return score

    def __str__(self):
        return self.name

