from rest_framework.pagination import PageNumberPagination


class BasicPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
