from django.shortcuts import redirect, reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import CreateReviewSerializer, ProductReviewsSerializer
from myapp.products import models as product_models
from . import models
from myapp.core.paginators import BasicPagination


"""
Review 관련 api

1. 특정 제품에 대한 리뷰

생성(POST) - 권한 : 로그인한 사람은 모두

읽기(GET) - 권한 : 로그인한 사람은 모두
-> 모두 읽으려할 때, 그 제품에 대한 리뷰를 작성하지 않으면 최대 1개밖에 못봄
리뷰를 1개라도 작성해야 모든 리뷰를 볼 수 있음

업데이트(PUT) - 권한 : 리뷰 작성자
삭제(DELETE) - 권한 : 리뷰 작성자

"""


class CreateReviewAPIView(CreateAPIView):
    """
    create reviews for specific products API Definition(POST)
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CreateReviewSerializer

    def post(self, request, product_id, **kwargs):
        return self.create(request, product_id, **kwargs)

    def create(self, request, product_id, **kwargs):
        serializer = CreateReviewSerializer(data=request.data)
        product = product_models.Product.objects.get_or_none(id=product_id)
        if not product:
            return Response(
                "product does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.is_valid():
            review = serializer.save(user=request.user, product=product)
            review_serializer = CreateReviewSerializer(review)
            return Response(data=review_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


class ProductReviewsAPIView(ListAPIView):
    """
    show reviews for specific products API Defintion(GET)
    """

    permission_classes = [IsAuthenticated]
    paginator = BasicPagination()
    serializer_class = ProductReviewsSerializer
    queryset = models.Review.objects.all()

    def get(self, request, product_id, **kwargs):
        return self.list(request, product_id, **kwargs)

    def list(self, request, product_id, **kwargs):
        # product = product_models.Product.objects.get_or_none(id=product_id)
        # if not product:
        #     return Response(
        #         "product does not exist", status=status.HTTP_400_BAD_REQUEST
        #     )
        reviews = models.Review.objects.filter(product__id__exact=product_id)
        page = self.paginate_queryset(reviews)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer._data)
