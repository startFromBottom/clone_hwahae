from collections import Counter
from django.shortcuts import redirect, reverse
from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ReviewSerializer, PhotoSerializer
from myapp.products import models as product_models
from . import models
from myapp.core.paginators import BasicPagination
from myapp.users import models as user_models


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
            user = user_models.User.objects.get_or_none(id=request.user.id)
            user.review_count += 1
            user.save()
            return Response(data=review_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewsAPIView(ListAPIView):
    """
    show reviews for specific product API Defintion(GET Only)
    """

    permission_classes = [IsAuthenticated]
    paginator = BasicPagination()
    serializer_class = ReviewSerializer
    queryset = models.Review.objects.all()

    def get_reviews_statistics(self, reviews: QuerySet) -> dict:

        review_scores = [review.score for review in reviews]
        average_score = round(sum(review_scores) / len(review_scores), 2)
        score_counter = dict(Counter(review_scores))

        return {
            "statistics": {
                "averge_score": average_score,
                "score_counter": score_counter,
            }
        }

    def get(self, request, product_id, **kwargs):
        return self.list(request, product_id, **kwargs)

    def list(self, request, product_id, **kwargs):
        qs = self.get_queryset()
        reviews = qs.filter(product__id__exact=product_id)
        if not reviews:
            return Response("reviews don't exist", status=status.HTTP_404_NOT_FOUND)
        reviews_statistics = self.get_reviews_statistics(reviews)
        print(reviews_statistics)

        page = self.paginate_queryset(reviews)
        serializer = self.get_serializer(page, many=True)
        user = user_models.User.objects.get_or_none(id=request.user.id)
        if user.review_count == 0:
            message = f"{str(user)} 님의 소중한 리뷰를 남겨주세요. "
            message += "내가 사용했던 화장품 리뷰 1개만 남기면 모든 리뷰를 확인할 수 있습니다."
            return Response([message, serializer.data])
        return Response([reviews_statistics, serializer.data])


class SpecificReviewAPIView(RetrieveUpdateDestroyAPIView):
    """
    retrieve, update, destory specific review API definition

    retrieve -> GET
    update -> PUT
    delete -> DELETE
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
        print(review.photo_urls())
        if not review:
            return Response("review does not exists", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            return Response(self.get_serializer(review).data, status=status.HTTP_200_OK)
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


class ScrapReviewAPIView(APIView):

    """ do or cancel scrap review API Definition (POST only) """

    def post(self, request, review_id):

        user = request.user
        review = models.Review.objects.get_or_none(id=review_id)
        if not review:
            return Response("review does not exist.", status=status.HTTP_404_NOT_FOUND)
        scrap_reviews = user.scrap_reviews.all()
        if review in scrap_reviews:
            # already exists -> cancel scrap
            user.scrap_reviews.remove(review)
            user.save()
            return Response("scrap is canceled", status=status.HTTP_200_OK)
        else:
            # scrap
            user.scrap_reviews.add(review)
            user.save()
            return Response("scrap ok", status=status.HTTP_200_OK)


class FavoriteReviewAPIView(APIView):

    """ Like or cancel review API Definition (POST, GET) """

    def post(self, request, review_id):

        user = request.user
        review = models.Review.objects.get_or_none(id=review_id)
        if not review:
            return Response("review does not exist.", status=status.HTTP_404_NOT_FOUND)
        favorite_users = review.favorite_users.all()
        if user in favorite_users:
            # already exists -> cancel favorite
            review.favorite_users.remove(user)
            review.save()
            return Response("Cancel like", status=status.HTTP_200_OK)
        else:
            # like
            review.favorite_users.add(user)
            review.save()
            return Response("Add like", status=status.HTTP_200_OK)

    def get(self, request, review_id):
        """
        show the number of favorites of review
        """
        review = models.Review.objects.get_or_none(id=review_id)
        if not review:
            return Response("review does not exist.", status=status.HTTP_404_NOT_FOUND)

        return Response(
            data={"num of favorites": review.num_favorites()}, status=status.HTTP_200_OK
        )


class ReviewCreatePhotosAPIView(CreateAPIView):
    """
    create photos for specific review API Definition(POST only)
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer
    queryset = models.Review.objects.all()

    def post(self, request, review_id):
        return self.create(request, review_id)

    def create(self, request, review_id):
        try:
            review = self.get_queryset().get(id=review_id)
        except models.Review.DoesNotExist:
            return Response("review does not exists", status=status.HTTP_404_NOT_FOUND)
        if request.user != review.user:
            return Response(
                "Not allowed to other users", status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(review=review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewSpecificPhotoAPIView(RetrieveUpdateDestroyAPIView):

    """ read / update / delete specific review's photos
    API Defintion """

    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer
    queryset = models.Review.objects.all()
    lookup_url_kwarg = "photo_id"

    def get_review(self, review_id):
        qs = self.get_queryset()
        try:
            review = qs.get(id=review_id)
            return review
        except models.Review.DoesNotExist:
            return None

    def get(self, request, review_id, photo_id):
        return self.retrieve(request, review_id, photo_id)

    def retrieve(self, request, review_id, photo_id):
        review = self.get_review(review_id)
        if not review:
            return Response("review does not exists", status=status.HTTP_404_NOT_FOUND)
        photo = models.Photo.objects.get_or_none(id=photo_id)
        if not photo:
            return Response("photo not exists", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(photo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, review_id, photo_id):
        return self.update(request, review_id, photo_id)

    def update(self, request, review_id, photo_id):
        review = self.get_review(review_id)
        if not review:
            return Response("review does not exists", status=status.HTTP_404_NOT_FOUND)
        if request.user != review.user:
            return Response(
                "Not allowed to other users", status=status.HTTP_403_FORBIDDEN
            )
        photo = models.Photo.objects.get_or_none(id=photo_id)
        if not photo:
            return Response("photo not exists", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(review=review)
            return Response(self.get_serializer(photo).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id, photo_id):
        return self.destroy(request, review_id, photo_id)

    def destory(self, request, review_id, photo_id):
        review = self.get_review(review_id)
        if not review:
            return Response("review does not exists", status=status.HTTP_404_NOT_FOUND)
        if request.user != review.user:
            return Response(
                "Not allowed to other users", status=status.HTTP_403_FORBIDDEN
            )
        photo = models.Photo.objects.get_or_none(id=photo_id)
        if not photo:
            return Response("photo not exists", status=status.HTTP_404_NOT_FOUND)
        photo.delete()
        return Response(status=status.HTTP_200_OK)

