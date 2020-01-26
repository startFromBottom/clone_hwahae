from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("myapp.products.urls", namespace="products")),
    path("users/", include("myapp.users.urls", namespace="users")),
    path("reviews/", include("myapp.reviews.urls", namespace="reviews")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
