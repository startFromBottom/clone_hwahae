from django.urls import path, reverse, include
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from .views import ProductsListAPIView, ProductDetailAPIView, SortProducts
from .queryparams_validators import ParamsCheck
from .serializers import (
    ProductsListSerializer,
    ProductDetailSerializer,
    Top3ProductsSerializer,
)


class ProdctsListAPITest(APITestCase, URLPatternsTestCase):

    """ all tests related with .views ProductsListAPI """

    urlpatterns = [path("products/", ProductsListAPIView.as_view(), name="products")]
    # urlpatterns = [path("", include("myapp.products.urls"))]

    def test_valid_param(self):
        url = reverse("products")
        query_params = "?skin_type=oily&category=skin_care"
        response = self.client.get(url + query_params, format="json")

        pass

    def test_contain_invalid_param(self):
        pass

    def test_have_skin_type_param(self):
        pass

    def test_valid_skin_type(self):
        pass

    def test_sort_products(self):
        """
        test views.Sortproducts class
        """
        pass


class ProductDetailAPITest(APITestCase, URLPatternsTestCase):

    """ all tests related with .views ProductDetailAPI """

    urlpatterns = [path("product/<int:product_pk>", ProductDetailAPI.as_view())]

    def test_aaa(self):

        assert 1 == 2

