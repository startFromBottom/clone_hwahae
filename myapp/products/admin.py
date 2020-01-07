from django.contrib import admin
from . import models


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    """ Ingredient Admin Definition """

    list_display = ("name", "oily", "dry", "sensitive", "ingredient_score")


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    """ Product Admin Definition """

    list_display = (
        "name",
        "monthlySales",
        "count_ingredients",
        "product_score",
    )
    list_filter = (
        "category",
        "gender",
    )

    ordering = ("-monthlySales",)

    def count_ingredients(self, obj):
        return obj.ingredients.count()

