from rest_framework import serializers
from .models import User
from myapp.products import models as product_models


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "username",
        )

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user


class UserFavsSerializer(serializers.ModelSerializer):

    favs_ingredients = serializers.CharField(source="favs_ingredients_str")
    favs_products = serializers.CharField(source="favs_products_str")

    class Meta:
        model = User
        fields = (
            "favs_products",
            "favs_ingredients",
        )

    def validate(self, data):
        """
        check data is validated, if validated, then update instance in
        self.update method
        """
        if not data:
            raise serializers.ValidationError("Input is None")

        if self.instance:  # update
            favs_products = data.get(
                "favs_products_str", self.instance.favs_products_str()
            )
            favs_ingredients = data.get(
                "favs_ingredients_str", self.instance.favs_ingredients_str()
            )
        else:  # create
            favs_products = data.get("favs_products_str", None)
            favs_ingredients = data.get("favs_ingredients_str", None)

        if favs_products is None or favs_ingredients is None:
            raise serializers.ValidationError("Input parameters invalid")

        for p_name in favs_products.split(","):
            product = product_models.Product.objects.get_or_none(name=p_name)
            if product is None:
                raise serializers.ValidationError(f"{p_name} is not registered product")

        for i_name in favs_ingredients.split(","):
            ingredient = product_models.Ingredient.objects.get_or_none(name=i_name)
            if ingredient is None:
                raise serializers.ValidationError(
                    f"{i_name} is not registered ingredient"
                )

        return data

    def update(self, instance, validated_data):
        favs_products = validated_data.get("favs_products_str", None)
        favs_ingredients = validated_data.get("favs_ingredients_str", None)

        product_ids = []
        for p_name in favs_products.split(","):
            product_ids.append(
                product_models.Product.objects.get_or_none(name=p_name).id
            )

        ingredient_ids = []
        for i_name in favs_ingredients.split(","):
            ingredient_ids.append(
                product_models.Ingredient.objects.get_or_none(name=i_name).id
            )

        instance.favs_products.set(product_ids)
        instance.favs_ingredients.set(ingredient_ids)
        instance.save()

        return instance
