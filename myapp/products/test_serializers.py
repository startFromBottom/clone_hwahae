from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .serializers import (
    ProductsListSerializer,
    ProductDetailSerializer,
    Top3ProductsSerializer,
)
from .models import Ingredient, Product
from myapp.users import models as user_models
from myapp.core.paginators import BasicPagination


class SerializerTest(APITestCase):
    """ 
    all tests related with ProductsListSerializer, ProductDetailSerializer,
    Top3ProductsSerializer Definition
    """

    @classmethod
    def setUpTestData(cls):
        """
        skin_type of all products : skincare
        test_data : same
        """
        user_models.User.objects.create(
            id=1, username="test_user", email="test@test.com", password="test1234",
        )

        Ingredient.objects.create(
            id=1, name="ingredient1", oily="O", dry="", sensitive="X"
        )
        Ingredient.objects.create(
            id=2, name="ingredient2", oily="O", dry="X", sensitive="O"
        )
        Ingredient.objects.create(
            id=3, name="ingredient3", oily="", dry="O", sensitive="X"
        )
        Ingredient.objects.create(
            id=4, name="ingredient4", oily="", dry="X", sensitive="O"
        )
        Ingredient.objects.create(
            id=5, name="ingredient5", oily="X", dry="O", sensitive=""
        )
        Ingredient.objects.create(
            id=6, name="ingredient6", oily="X", dry="", sensitive="O"
        )
        products_related_ingredients = [
            [
                Ingredient.objects.get(id=1),
                Ingredient.objects.get(id=2),
                Ingredient.objects.get(id=3),
            ],
            [
                Ingredient.objects.get(id=2),
                Ingredient.objects.get(id=4),
                Ingredient.objects.get(id=6),
            ],
            [Ingredient.objects.get(id=3), Ingredient.objects.get(id=5),],
            [
                Ingredient.objects.get(id=2),
                Ingredient.objects.get(id=3),
                Ingredient.objects.get(id=4),
                Ingredient.objects.get(id=5),
            ],
        ]

        for i in range(1, 5):
            instance = Product.objects.create(
                id=i,
                imageId=f"image-{i}",
                name=f"name-{i}",
                price=i * 1000,
                gender="male" if i % 2 == 0 else "female",
                category="skincare",
                monthlySales=i * 5000,
            )
            instance.ingredients.set(products_related_ingredients[i - 1])

    def test_productsListSerializer_contains_expected_fields(self):
        products = Product.objects.all()
        data = ProductsListSerializer(products, many=True).data
        self.assertEqual(len(data), 4)
        for each in data:
            self.assertEqual(
                set(each.keys()),
                set(["id", "imgUrl", "name", "price", "ingredients", "monthlySales"]),
            )

    def test_productsDetailSerializer_contains_expected_fields(self):
        products = Product.objects.all()
        data = ProductDetailSerializer(products, many=True).data
        self.assertEqual(len(data), 4)
        for each in data:
            self.assertEqual(
                set(each.keys()),
                set(
                    [
                        "id",
                        "imgUrl",
                        "name",
                        "price",
                        "gender",
                        "category",
                        "ingredients",
                        "monthlySales",
                    ]
                ),
            )

    def test_Top3ProductsSerializer_contains_expected_fields(self):
        products = Product.objects.all()
        data = Top3ProductsSerializer(products, many=True).data
        self.assertEqual(len(data), 4)
        for each in data:
            self.assertEqual(
                set(each.keys()), set(["id", "imgUrl", "name", "price"]),
            )
