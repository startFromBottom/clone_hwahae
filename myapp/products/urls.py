from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("products/", views.ProductsListView.as_view()),
    path("product/<int:product_pk>", views.ProductDetailView.as_view()),
]

