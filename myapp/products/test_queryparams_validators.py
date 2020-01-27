from rest_framework.test import APITestCase
from .queryparams_validators import ParamsCheck, APIParams


class ProductsListParamsCheckTest(APITestCase):

    """ ProductsListAPIViews's request query parameters test definition """

    possible_params = APIParams.products_list_params

    def test_param_valid(self):
        query_params = {
            "skin_type": "oily",
            "exclude_ingredient": "test",
            "include_ingredient": "test1",
        }
        result = ParamsCheck.validate(query_params, self.possible_params)
        self.assertEquals(result, False)

    def test_contain_invalid_param(self):
        query_params = {
            "skin_type": "oily",
            "category": "skincare",
            "something": "test",
        }
        string = ", ".join(self.possible_params)
        response = ParamsCheck.validate(query_params, self.possible_params)
        message = (
            f"invalid query parameters. query parameters must be included in {string}"
        )
        self.assertEquals(response.data, message)

    def test_not_have_skin_type_param(self):
        query_params = {
            "category": "skincare",
            "exclude_ingredient": "a",
            "include_ingredient": "b",
        }
        response = ParamsCheck.validate(query_params, self.possible_params)
        message = "Request url must contain the skin_type parameter"
        self.assertEquals(response.data, message)

    def test_invalid_skin_type(self):
        query_params = {
            "category": "skin_care",
            "skin_type": "something",
        }
        response = ParamsCheck.validate(query_params, self.possible_params)
        message = "skin type must be one of dry, sensitive, oily"
        self.assertEquals(response.data, message)


class ProductDetailParamsCheckTest(APITestCase):

    """ ProductDetailAPIViews's request query parameters test definition """

    possible_params = APIParams.product_detail_params

    def test_param_valid(self):
        """ fail test 
        this test should be fail because possible_params are not same with
        ProductsListAPI's possible_params
        """
        query_params = {
            "skin_type": "oily",
            "exclude_ingredient": "test",
            "include_ingredient": "test1",
        }
        result = ParamsCheck.validate(query_params, self.possible_params)
        self.assertNotEquals(result, False)

    def test_contain_invalid_param(self):
        query_params = {
            "skin_type": "oily",
            "category": "skincare",
            "something": "test",
        }
        string = ", ".join(self.possible_params)
        response = ParamsCheck.validate(query_params, self.possible_params)
        message = (
            f"invalid query parameters. query parameters must be included in {string}"
        )
        self.assertEquals(response.data, message)

    def test_not_have_skin_type_param(self):
        query_params = {
            "category": "skincare",
            "exclude_ingredient": "a",
            "include_ingredient": "b",
        }
        response = ParamsCheck.validate(query_params, self.possible_params)
        message = (
            "invalid query parameters. query parameters must be included in skin_type"
        )
        self.assertEquals(response.data, message)

    def test_invalid_skin_type(self):
        query_params = {
            "category": "skin_care",
            "skin_type": "something",
        }
        string = ", ".join(self.possible_params)
        response = ParamsCheck.validate(query_params, self.possible_params)
        message = (
            f"invalid query parameters. query parameters must be included in {string}"
        )
        self.assertEquals(response.data, message)
