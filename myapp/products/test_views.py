from django.urls import path, reverse
from rest_framework.test import (
    APITestCase,
    URLPatternsTestCase,
    APIRequestFactory,
    force_authenticate,
)
from .views import ProductsListAPIView, ProductDetailAPIView
from .models import Ingredient, Product
from myapp.users import models as user_models


class SetUp:
    @classmethod
    def setUpTestData(cls):
        """
        skin_type of all products : skincare
        use same test data in ProductsListAPIViewTest, ProductDetailAPIViewTest
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


class ProductsListAPIViewTest(APITestCase, URLPatternsTestCase):

    """ all tests related with ProductsListAPIView Definition """

    urlpatterns = [path("products/", ProductsListAPIView.as_view(), name="products")]

    @classmethod
    def setUpTestData(cls):
        SetUp.setUpTestData()

    def test_filter_category_skincare_not_login(self):
        """ 
        fail test
        this test should be failed, because not authenticated
        """
        url = reverse("products")
        params = {"category": "skincare"}
        response = self.client.get(url, params=params)
        self.assertNotEquals(response.status_code, 200)

    def test_filter_by_category_skincare_with_login(self):
        factory = APIRequestFactory()
        view = ProductsListAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        skin_types = ["oily", "dry", "sensitive"]
        for skin_type in skin_types:
            # skin_type : not query params, used in sorting, so
            # responses must be same
            url = f"products/?skin_type={skin_type}&category=skincare"
            request = factory.get(url)
            force_authenticate(request, user=user)
            response = view(request)
            self.assertEquals(response.status_code, 200)
            self.assertEquals(len(response.data), 4)

    def test_filter_by_category_not_skincare(self):
        factory = APIRequestFactory()
        view = ProductsListAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = f"products/?skin_type=oily&category=maskpack"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEquals(response.status_code, 404)

    def test_clean_string(self):
        """ test ProductsListAPIView._clean_string method """
        params = "calf,morale"
        result = ProductsListAPIView._clean_string(self, string=params)
        self.assertEquals(result, ["calf", "morale"])

    def test_pagination(self):
        pass

    def test_pagination_404(self):
        """
        the number of products is four and BasicPagination.page_size=50
        -> if page=2 in request's query parameters, response.status_code will be 404
        """
        factory = APIRequestFactory()
        view = ProductsListAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = f"products/?skin_type=oily&page=2"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEquals(response.status_code, 404)

    def test_filter_include_ingredient(self):
        """
        include ingredient2 test
        expected_results : name-1, name-2, name-4
        """
        factory = APIRequestFactory()
        view = ProductsListAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = (
            f"products/?skin_type=oily&category=skincare&include_ingredient=ingredient2"
        )
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEquals(response.status_code, 200)
        expected = ["name-1", "name-2", "name-4"]
        for i, each in enumerate(response.data):
            self.assertEquals(each.get("name"), expected[i])

    def test_filter_exclude_ingredient_case1(self):
        """
        exclude ingredient4 test
        expected_results : name-1, name-3
        """
        factory = APIRequestFactory()
        view = ProductsListAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = (
            f"products/?skin_type=oily&category=skincare&exclude_ingredient=ingredient4"
        )
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEquals(response.status_code, 200)
        expected = ["name-1", "name-3"]
        for i, each in enumerate(response.data):
            self.assertEquals(each.get("name"), expected[i])

    def test_filter_exclude_ingredient_case2(self):
        """
        exclude ingredient2, ingredient6 test
        expected_results : name-2
        """
        factory = APIRequestFactory()
        view = ProductsListAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = f"products/?skin_type=oily&category=skincare&exclude_ingredient=ingredient2,ingredient6"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEquals(response.status_code, 200)
        expected = ["name-3"]
        for i, each in enumerate(response.data):
            self.assertEquals(each.get("name"), expected[i])

    def test_filter_both_include_and_exclude(self):
        """
        include ingredient2, exclude ingredient5 test
        expected_result : name-1, name-2
        """
        factory = APIRequestFactory()
        view = ProductsListAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = f"products/?skin_type=oily&category=skincare&include_ingredient=ingredient2&exclude_ingredient=ingredient5"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEquals(response.status_code, 200)
        expected = ["name-1", "name-2"]
        for i, each in enumerate(response.data):
            self.assertEquals(each.get("name"), expected[i])

    def test_filter_both_include_and_exclude_404(self):
        """
        include ingredient1, exclude ingredient3 test
        expected_result : 404 status
        """
        factory = APIRequestFactory()
        view = ProductsListAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = f"products/?skin_type=oily&category=skincare&include_ingredient=ingredient1&exclude_ingredient=ingredient3"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEquals(response.status_code, 404)

    def test_sort_products_skintype_oily(self):
        """
        sort order test (case oily)

        sort product by following criterias
        1) skin_type's score(Descending Order)
        2) price(Ascending Order)

                    oily_score   price
        product 1       2        1000
        product 2       0        2000 
        product 3       -1       3000
        product 4       0        4000

        -> expected result : 1-2-4-3
        """
        factory = APIRequestFactory()
        view = ProductsListAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = "products/?skin_type=oily&category=skincare"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 4)
        expected = ["name-1", "name-2", "name-4", "name-3"]
        for i, each in enumerate(response.data):
            self.assertEquals(each.get("name"), expected[i])

    def test_sort_products_skintype_dry(self):
        """
        sort order test (case dry)

        sort product by following criterias
        1) skin_type's score(Descending Order)
        2) price(Ascending Order)

                    dry_score    price
        product 1       0        1000
        product 2       -2       2000
        product 3       2        3000
        product 4       0        4000

        -> expected result : 3-1-4-2
        """
        factory = APIRequestFactory()
        view = ProductsListAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = "products/?skin_type=dry&category=skincare"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 4)
        expected = ["name-3", "name-1", "name-4", "name-2"]
        for i, each in enumerate(response.data):
            self.assertEquals(each.get("name"), expected[i])

    def test_sort_products_skintype_sensitive(self):
        """
        sort order test (case dry)

        sort product by following criterias
        1) skin_type's score(Descending Order)
        2) price(Ascending Order)

                    sensitive_score    price
        product 1       -1             1000
        product 2       3              2000
        product 3       -1             3000
        product 4       1              4000

        -> expected result : 2-4-1-3
        """
        factory = APIRequestFactory()
        view = ProductsListAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = "products/?skin_type=sensitive&category=skincare"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 4)
        expected = ["name-2", "name-4", "name-1", "name-3"]
        for i, each in enumerate(response.data):
            self.assertEquals(each.get("name"), expected[i])


class ProductDetailAPIViewTest(APITestCase, URLPatternsTestCase):

    """ all tests related with ProductDetailAPIView Definition """

    urlpatterns = [
        path(
            "product/<int:product_pk>",
            ProductDetailAPIView.as_view(),
            name="product-detail",
        )
    ]

    @classmethod
    def setUpTestData(cls):
        SetUp.setUpTestData()

    def test_get_data_by_pk_not_login(self):
        """ 
        fail test
        this test should be failed, because not authenticated
        """
        url = reverse("product-detail", kwargs={"product_pk": 1})
        params = {"skin_type": "oily"}
        response = self.client.get(url, params=params)
        self.assertNotEquals(response.status_code, 200)

    def test_get_data_by_pk_login(self):
        factory = APIRequestFactory()
        view = ProductDetailAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = f"product/1?skin_type=oily"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, product_pk=1)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 4)
        self.assertEquals(response.data[0].get("name"), "name-1")

    def test_get_top3_skin_type_oily(self):
        """
        sort products and get top3

        sort product by following criterias(same with ProductsListAPIView)
        1) skin_type's score(Descending Order)
        2) price(Ascending Order)

                    oily_score   price
        product 1       2        1000
        product 2       0        2000 
        product 3       -1       3000
        product 4       0        4000

        -> expected result : 1-1-2-4 (first : product_pk=1 in request params)
        """
        product_pk = 1
        factory = APIRequestFactory()
        view = ProductDetailAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = f"product/{product_pk}?skin_type=oily"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, product_pk=product_pk)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 4)
        expected = ["name-1", "name-1", "name-2", "name-4"]
        real = [each.get("name") for each in response.data]
        self.assertEquals(expected, real)

    def test_get_top3_skin_type_dry(self):
        """
        sort order and get top3

        sort product by following criterias(same with ProductsListAPIView)
        1) skin_type's score(Descending Order)
        2) price(Ascending Order)

                    dry_score    price
        product 1       0        1000
        product 2       -2       2000
        product 3       2        3000
        product 4       0        4000

        -> expected result : 1-3-1-4 (first : product_pk=1 in request params)
        """
        product_pk = 1
        factory = APIRequestFactory()
        view = ProductDetailAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = f"product/{product_pk}?skin_type=dry"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, product_pk=product_pk)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 4)
        expected = ["name-1", "name-3", "name-1", "name-4"]
        real = [each.get("name") for each in response.data]
        self.assertEquals(expected, real)

    def test_get_top3_skin_type_sensitive(self):
        """
        sort order test and get top3

        sort product by following criterias
        1) skin_type's score(Descending Order)
        2) price(Ascending Order)

                    sensitive_score    price
        product 1       -1             1000
        product 2       3              2000
        product 3       -1             3000
        product 4       1              4000

        -> expected result : 1-2-4-1 (first : product_pk=1 in request params)
        """
        product_pk = 1
        factory = APIRequestFactory()
        view = ProductDetailAPIView.as_view()
        user = user_models.User.objects.get(username="test_user")
        url = f"product/{product_pk}?skin_type=sensitive"
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request, product_pk=product_pk)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 4)
        expected = ["name-1", "name-2", "name-4", "name-1"]
        real = [each.get("name") for each in response.data]
        self.assertEquals(expected, real)
