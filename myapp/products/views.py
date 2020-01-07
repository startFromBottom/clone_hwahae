from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import server_error, ValidationError
from .models import Ingredient, Product, OtherCharException
from .serializers import ProductsListSerializer


# class NotSkinTypeException(Exception):
#     pass


class BasicPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"


class SortProducts:
    @staticmethod
    def sort_products(param: str, querySet: QuerySet):
        """
        sort product by using skin_type's score(Descending Order)
        and monthlySales(Ascending Order)
        """
        try:
            products_list = list(querySet)
            products_list.sort(  # if data size is bigger, this code will be inefficient..?
                key=lambda x: (-x.calculate_score(param), x.monthlySales)
            )
        except TypeError:
            return Response(
                "Request url must contain the skin_type parameter",
                status=status.HTTP_400_BAD_REQUEST,
            )
        return products_list


class ProductsListView(ListAPIView):

    paginator = BasicPagination()
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer

    def filter_queryset(self, queryset):
        """
        Filtering data according to Programmer's requirements,
        (ordering data will be handled in self.list method)

        <Query parameters from request>
        1. skin_type : only check None or not None -> will be handled in self.list method
        2. category : filter_query
        3. include_ingredients: filter_query
        4. exclude_ingredients: filter_qery
        5. page : not handled(Instead, use django's paginator)

        """
        products_qs = self.get_queryset()
        skin_type = self.request.query_params.get("skin_type")

        if skin_type is not None:
            category = self.request.query_params.get("category", None)
            exclude_ingredients = self.request.query_params.get(
                "exclude_ingredient", None
            )
            exclude_ingredients = ProductsListView._clean_string(exclude_ingredients)
            include_ingredients = self.request.query_params.get(
                "include_ingredient", None
            )
            include_ingredients = ProductsListView._clean_string(include_ingredients)

            # filtering part
            for each in include_ingredients:
                products_qs = products_qs.filter(ingredients__name=each)
            for each in exclude_ingredients:
                products_qs = products_qs.exclude(ingredients__name=each)

            return products_qs

        return None

    def list(self, request):
        """
        get queryset from self.filter_queryset.

        - do exception handling of skin_type,
        - order by using skin_type's score(Descending Order) and monthlySales(Ascending Order)
        - pagination

        """
        skin_type = self.request.query_params.get("skin_type")
        if skin_type is not None:
            products_list = SortProducts.sort_products(
                param=skin_type, querySet=self.filter_queryset(self.get_queryset())
            )
            page = self.paginate_queryset(products_list)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)
        return

    @staticmethod
    def _clean_string(string):
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


class ProductDetailView(APIView):
    def get(self, request, product_pk):
        # 특정 상품 조회
        product = Product.objects.get(id=product_pk)
        # top 3 products
        products_qs = Product.objects.filter(category=product.category)
        skin_type = request.query_params.get("skin_type", None)

        products_list = SortProducts.sort_products(
            param=skin_type, querySet=products_qs
        )
        products_list = products_list[:3]

        return Response(status=status.HTTP_200_OK)
