from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import server_error, ValidationError
from .models import Ingredient, Product
from .queryparams_validators import ParamsCheck, APIParams
from .serializers import (
    ProductsListSerializer,
    ProductDetailSerializer,
    Top3ProductsSerializer,
)


@api_view(["GET"])
def main(request):
    return Response("main page")


class BasicPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"


class SortProducts:

    """ Sort Products class Definition """

    @staticmethod
    def sort_products(param: str, querySet: QuerySet):
        """
        sort product by following criterias
        1) skin_type's score(Descending Order)
        2) monthlySales(Ascending Order)
        """
        products_list = list(querySet)
        products_list.sort(  # if data size is bigger, this code will be inefficient..?
            key=lambda x: (-x.calculate_score(param), x.monthlySales)
        )
        return products_list


class ProductsListAPIView(ListAPIView):

    """ list of products API Definition """

    permission_classes = [IsAuthenticated]

    paginator = BasicPagination()
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer

    def filter_queryset(self, queryset):
        """
        Filtering data according to Programmer's requirements,
        (ordering data and send response part will be handled in self.list method)

        also, Exceptions will be handled in self.list method

        <Query parameters from request>
        1. skin_type : handled in ParamsCheck.validate method 
        2. category : filter_query
        3. include_ingredients: filter_query
        4. exclude_ingredients: filter_query
        5. page : not handled directly(Instead, use django's paginator)

        """
        query_params = self.request.query_params
        # validate
        exception_response = ParamsCheck.validate(
            query_params, APIParams.products_list_params
        )
        if exception_response:
            return exception_response

        products_qs = self.get_queryset()
        skin_type = query_params.get("skin_type")

        category = query_params.get("category", None)
        exclude_ingredients = query_params.get("exclude_ingredient", None)
        exclude_ingredients = self._clean_string(exclude_ingredients)
        include_ingredients = query_params.get("include_ingredient", None)
        include_ingredients = self._clean_string(include_ingredients)

        # filtering part
        if category is not None:
            products_qs = products_qs.filter(category=category)
        for each in include_ingredients:
            products_qs = products_qs.filter(ingredients__name=each)
        for each in exclude_ingredients:
            products_qs = products_qs.exclude(ingredients__name=each)

        return products_qs

    def list(self, request):
        """
        get queryset from self.filter_queryset, then send response

        - do exception handlings of self.filter_queryset method
        - order by using skin_type's score(Descending Order) and monthlySales(Ascending Order)
        - pagination

        """
        skin_type = self.request.query_params.get("skin_type")
        queryset = self.filter_queryset(self.get_queryset())
        if isinstance(queryset, Response):  # exception
            return queryset
        products_list = SortProducts.sort_products(param=skin_type, querySet=queryset)
        page = self.paginate_queryset(products_list)
        if len(page) != 0:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response("Can't find data", status=status.HTTP_404_NOT_FOUND)

    def _clean_string(self, string):
        """
        convert string to list
        ex)
        'calf, morale' -> ['calf', 'morale']
        """
        if string is None:
            return []
        str_list = string.strip().split(",")
        str_list = [each.strip() for each in str_list]
        return str_list


class ProductDetailAPIView(APIView):

    """ show detail of product and top3 score products API Definition """

    permission_classes = [IsAuthenticated]

    def get(self, request, product_pk):

        query_params = request.query_params
        exception_response = ParamsCheck.validate(
            query_params, APIParams.product_detail_params
        )
        if exception_response:
            return exception_response
        # product detail
        try:
            product = Product.objects.get(id=product_pk)
        except Product.DoesNotExist:
            return Response("can't find data", status=status.HTTP_404_NOT_FOUND)

        # top 3 products
        products_qs = Product.objects.filter(category=product.category)
        skin_type = query_params.get("skin_type")
        products_list = SortProducts.sort_products(
            param=skin_type, querySet=products_qs
        )
        products_list = products_list[:3]

        product_detail_data = ProductDetailSerializer(product).data
        top3_products_data = Top3ProductsSerializer(products_list, many=True).data
        data = [product_detail_data] + top3_products_data

        return Response(data=data, status=status.HTTP_200_OK)
