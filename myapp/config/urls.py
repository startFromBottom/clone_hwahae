import os
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Clone HwaHae API",
        default_version="v1",
        description="API documents of programmers server challenge",
        contact=openapi.Contact(email="lucky807@korea.ac.kr"),
    ),
    validators=["flex"],
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path(os.environ.get("ADMIN") + "/", admin.site.urls),
    path("", include("myapp.products.urls", namespace="products")),
    path("users/", include("myapp.users.urls", namespace="users")),
    path("reviews/", include("myapp.reviews.urls", namespace="reviews")),
    path(
        "swagger/v1/",
        schema_view_v1.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/v1/",
        schema_view_v1.with_ui("redoc", cache_timeout=0),
        name="schema-redoc-ui",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("debug/", include(debug_toolbar.urls))]
