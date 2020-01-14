from django.urls import path
from . import views

app_name = "users"


urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("login/naver/", views.login_naver, name="login-naver"),
    path("login/naver/callback/", views.naver_callback, name="naver-callback"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpAPIView.as_view(), name="signup"),
    path("me/", views.MeView.as_view(), name="me"),
]

