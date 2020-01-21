from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path(
        "create/<int:product_id>",
        views.CreateReviewAPIView.as_view(),
        name="create-review",
    ),
    path(
        "product/<int:product_id>/",
        views.ProductReviewsAPIView.as_view(),
        name="product-reviews",
    ),
]
