from rest_framework import serializers
from .models import Product


class ProductsListSerializer(serializers.ModelSerializer):
    ingredients = serializers.CharField(source="ingredient_str")

    class Meta:
        model = Product
        fields = [
            "id",
            "imgUrl",
            "name",
            "price",
            "ingredients",
            "monthlySales",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):

    ingredients = serializers.CharField(source="ingredient_str")

    class Meta:
        model = Product
        fields = [
            "id",
            # "imgUrl",
            "name",
            "price",
            "gender",
            "category",
            "ingredients",
            "monthlySales",
        ]

    def is_valid(self):
        return super().is_valid()


class Top3ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "imgUrl", "name", "price")

    def is_valid(self):
        return super().is_valid()
