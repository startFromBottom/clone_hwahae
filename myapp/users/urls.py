from django.urls import path
from . import views

app_name = "users"


urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("verify/<str:key>/", views.complete_verification, name="verify-email"),
    path("login/naver/", views.login_naver, name="login-naver"),
    path(
        "login/naver/callback/",
        views.NaverLoginCallback.as_view(),
        name="naver-callback",
    ),
    path("login/facebook/", views.login_facebook, name="login-facebook"),
    path(
        "login/facebook/callback/",
        views.FacebookLoginCallback.as_view(),
        name="facebook-callback",
    ),
    path("login/google/", views.login_google, name="login-google"),
    path(
        "login/google/callback/",
        views.GoogleLoginCallback.as_view(),
        name="google-callback",
    ),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpAPIView.as_view(), name="signup"),
    path("me/", views.MeView.as_view(), name="me"),
    path("me/reviews/", views.MeReviewsView.as_view(), name="me-reviews"),
    path("me/favs/", views.MeFavsView.as_view(), name="me-favs"),
    path("me/scraps/", views.MeScrapsView.as_view(), name="me-scraps"),
    path(
        "me/scraps/<int:review_id>/",
        views.MeSpecificScrapView.as_view(),
        name="me-scrap",
    ),
]
