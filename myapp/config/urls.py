from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("myapp.products.urls")),
    path("users/", include("myapp.users.urls")),
]

