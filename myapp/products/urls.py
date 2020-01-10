from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("products/", views.ProductsListAPIView.as_view(), name="products"),
    path(
        "product/<int:product_pk>",
        views.ProductDetailAPIView.as_view(),
        name="product_detail",
    ),
]

