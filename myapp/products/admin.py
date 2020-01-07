from django.contrib import admin
from . import models


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    """ Ingredient Admin Definition """

    list_display = (
        "name",
        "oily",
        "dry",
        "sensitive",
    )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    """ Product Admin Definition """

    list_display = (
        "name",
        "category",
        "monthlySales",
        "show_ingredients",
        "oily_score",
        "dry_score",
        "sensitive_score",
    )
    list_filter = (
        "category",
        "gender",
    )

    search_fields = ("=name",)

    ordering = ("-monthlySales",)

    def show_ingredients(self, obj):
        return [each.name for each in obj.ingredients.all()]

    def oily_score(self, obj):
        return sum(
            [obj.convert_char_to_score(each.oily) for each in obj.ingredients.all()]
        )

    def dry_score(self, obj):
        return sum(
            [obj.convert_char_to_score(each.dry) for each in obj.ingredients.all()]
        )

    def sensitive_score(self, obj):
        return sum(
            [
                obj.convert_char_to_score(each.sensitive)
                for each in obj.ingredients.all()
            ]
        )
