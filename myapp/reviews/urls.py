from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path(
        "create/<int:product_id>/",
        views.CreateReviewAPIView.as_view(),
        name="create-review",
    ),
    path(
        "product/<int:product_id>/",
        views.ProductReviewsAPIView.as_view(),
        name="product-reviews",
    ),
    path("<int:review_id>/", views.ReviewAPIView.as_view(), name="review",),
    path(
        "<int:review_id>/scrap", views.ScrapReviewAPIView.as_view(), name="scrap-review"
    ),
    path(
        "<int:review_id>/favs/",
        views.FavoriteReviewAPIView.as_view(),
        name="favorite-review",
    ),
]
