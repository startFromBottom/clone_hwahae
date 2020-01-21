from django.shortcuts import redirect, reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ReviewSerializer
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
    create reviews for specific product API Definition(POST only)
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def post(self, request, product_id, **kwargs):
        return self.create(request, product_id, **kwargs)

    def create(self, request, product_id, **kwargs):
        serializer = self.get_serializer(data=request.data)
        product = product_models.Product.objects.get_or_none(id=product_id)
        if not product:
            return Response(
                "product does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.is_valid():
            review = serializer.save(user=request.user, product=product)
            review_serializer = ReviewSerializer(review)
            return Response(data=review_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


class ProductReviewsAPIView(ListAPIView):
    """
    show reviews for specific product API Defintion(GET)
    """

    permission_classes = [IsAuthenticated]
    paginator = BasicPagination()
    serializer_class = ReviewSerializer
    queryset = models.Review.objects.all()

    def get(self, request, product_id, **kwargs):
        return self.list(request, product_id, **kwargs)

    def list(self, request, product_id, **kwargs):
        qs = self.get_queryset()
        reviews = qs.filter(product__id__exact=product_id)
        page = self.paginate_queryset(reviews)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class ReviewAPIView(RetrieveUpdateDestroyAPIView):
    """
    retrieve, update, delete specific review API definition(GET, PUT, DELETE)
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    queryset = models.Review.objects.all()
    lookup_url_kwarg = "review_id"

    def get_review(self, review_id):
        qs = self.get_queryset()
        try:
            review = qs.get(id=review_id)
            return review
        except models.Review.DoesNotExist:
            return None

    def get(self, request, review_id, **kwargs):
        return self.retrieve(request, review_id, **kwargs)

    def retrieve(self, request, review_id, **kwargs):
        review = self.get_review(review_id)
        if not review:
            return Response("review does not exists", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(review)
        return Response(serializer.data)

    def put(self, request, review_id, **kwargs):
        return self.update(request, review_id, **kwargs)

    def update(self, request, review_id, **kwargs):
        review = self.get_review(review_id)
        if not review:
            return Response("review does not exists", status=status.HTTP_404_NOT_FOUND)
        if review.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(review)
        if serializer.is_valid():
            review = serializer.save()
            return Response(self.get_serializer(review).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id, **kwargs):
        return self.destroy(request, review_id, **kwargs)

    def destory(self, request, review_id, **kwargs):
        review = self.get_review(review_id)
        if not review:
            return Response("review does not exists", status=status.HTTP_404_NOT_FOUND)
        if review.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        review.delete()
        return Response(status=status.HTTP_200_OK)
