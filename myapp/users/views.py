import os
import requests
import jwt
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer,
    UserFavsSerializer,
    MeScrapsSerializer,
    MeReviewsSerializer,
)
from . import models
from . import mixins
from myapp.core.paginators import BasicPagination
from myapp.reviews import serializers as review_serializers
from myapp.reviews import models as review_models


def log_out(request):
    logout(request)
    return redirect(reverse("users:login"))


def complete_verification(request, key):

    """ Email Verification function """

    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except models.User.DoesNotExist:
        pass

    return redirect(reverse("products:main"))


class SignUpAPIView(CreateAPIView):

    """ Sign up By Email API View Definition """

    serializer_class = UserSerializer

    def post(self, request):
        return self.create(request)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            login(request, new_user)
            new_user.verify_email()
            return Response(UserSerializer(new_user).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    """ Log in By Email API View Definition """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.id}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


def login_naver(request):
    """
    reference : https://developers.naver.com/docs/login/api/
    """
    client_id = os.environ.get("NAVER_ID")
    state = "RANDOM_STATE"
    # Authorization callback URL
    redirect_uri = "https://127.0.0.1:8000/users/login/naver/callback/"
    header = {"Content-Type": "application/json"}

    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}\
            &redirect_uri={redirect_uri}&state={state}",
        header=header,
    )


class NaverException(Exception):
    pass


class NaverLoginCallback(mixins.LoginCallbackMixin, APIView):
    def __init__(self, *args, **kwargs):
        self.error_message = ""
        return super().__init__(*args, **kwargs)

    def get(self, request):
        try:
            access_token = self.get_access_token(request)
            profile_response = self.get_userinfo_from_access_token(access_token)
            response = self.check_user_and_login(request, profile_response)
            return response
        except NaverException:
            return Response(self.error_message, status=status.HTTP_400_BAD_REQUEST)

    def get_access_token(self, request) -> str or Exception:
        """
        reference : https://developers.naver.com/docs/login/api/
        """
        client_id = os.environ.get("NAVER_ID")
        client_secret = os.environ.get("NAVER_SECRET")
        state = request.GET.get("state", None)
        redirect_uri = "https://127.0.0.1:8000/users/login/naver/callback/"
        code = request.GET.get("code", None)
        if code is None:
            self.error_message = "Can't get code info"
            raise NaverException(self.error_message)
        api_url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}&state={state}"
        result = requests.get(
            api_url,
            headers={
                "X-Naver-Client-Id": client_id,
                "X-Naver-Client-Secret": client_secret,
            },
        )
        result_json = result.json()
        error = result_json.get("error", None)
        if error is not None:
            self.error_message = "Can't get access token"
            raise NaverException(self.error_message)
        access_token = result_json.get("access_token")

        return access_token

    def get_userinfo_from_access_token(self, access_token: str):
        header = "Bearer " + access_token
        api_url = "https://openapi.naver.com/v1/nid/me"
        profile_json = requests.get(api_url, headers={"Authorization": header}).json()
        profile_response = profile_json.get("response")
        if profile_response is not None:
            return profile_response
        else:
            self.error_message = "profile does not exist"
            raise NaverException(self.error_message)

    def check_user_and_login(self, request, profile_response) -> Response:
        name = profile_response.get("name")
        email = profile_response.get("email")
        # birthday = profile_response.get("birthday")
        gender = profile_response.get("gender")
        nickname = profile_response.get("nickname")
        # check user already exists
        user = models.User.objects.get_or_none(email=email)
        if user is not None:
            if user.login_method != models.User.LOGIN_NAVER:
                error_message = f"Please log in with: {user.login_method}"
                raise NaverException(error_message)
        else:
            # create new user
            user = models.User.objects.create(
                email=email,
                username=name,
                login_method=models.User.LOGIN_NAVER,
                nickname=nickname,
                gender=models.User.GENDER_MALE
                if gender == "M"
                else models.User.GENDER_FEMALE,
                email_verified=True,
            )
        login(request, user)

        return Response("Naver login Succeed!")


def login_facebook(request):
    """
    - reference
    https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow
    
    must use https
    """
    client_id = os.environ.get("FACEBOOK_ID")
    redirect_uri = "https://127.0.0.1:8000/users/login/facebook/callback/"
    state = "{st=state123abc,ds=123456789}"

    return redirect(
        f"https://www.facebook.com/v5.0/dialog/oauth?client_id={client_id}&redirect_uri={redirect_uri}&state={state}"
    )


class FacebookException(Exception):
    pass


class FacebookLoginCallback(mixins.LoginCallbackMixin, APIView):
    """
    - reference
    https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow
    """

    def __init__(self, *args, **kwargs):
        self.error_message = ""
        return super().__init__(*args, **kwargs)

    def get(self, request):
        try:
            access_token = self.get_access_token(request)
            profile_response = self.get_userinfo_from_access_token(access_token)
            response = self.check_user_and_login(request, profile_response)
            return response
        except FacebookException:
            return Response(self.error_message, status=status.HTTP_400_BAD_REQUEST)

    def get_access_token(self, request) -> str or Exception:
        client_id = os.environ.get("FACEBOOK_ID")
        client_secret = os.environ.get("FACEBOOK_SECRET")
        redirect_uri = "https://127.0.0.1:8000/users/login/facebook/callback/"
        code = request.GET.get("code", None)

        if code is None:
            error_message = "Can't get code info"
            raise FacebookException(error_message)

        api_url = f"https://graph.facebook.com/v5.0/oauth/access_token?client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}"
        result = requests.get(api_url)
        result_json = result.json()
        error = result_json.get("error", None)

        if error is not None:
            self.error_message = "Can't get access token"
            raise FacebookException(self.error_message)

        # get access token(https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow)
        access_token = result_json.get("access_token")
        return access_token

    def get_userinfo_from_access_token(self, access_token: str):
        # 1. get user id by using access token
        url = f"https://graph.facebook.com/debug_token?input_token={access_token}&access_token={access_token}"
        data = requests.get(url).json()
        user_id = data.get("data").get("user_id")
        # 2. get profile data by using access_token and user_id
        # fields : https://developers.facebook.com/docs/graph-api/reference/user
        url = f"https://graph.facebook.com/v5.0/{user_id}?fields=email,first_name,last_name,birthday,age_range,gender&access_token={access_token}"
        profile_response = requests.get(url).json()
        error = profile_response.get("error")
        if error is not None:
            self.error_message = error.get("message")
            raise FacebookException(self.error_message)
        return profile_response

    def check_user_and_login(self, request, profile_response) -> Response:
        email = profile_response.get("email", None)
        first_name = profile_response.get("first_name", None)
        last_name = profile_response.get("last_name", None)
        # birthday = profile_response.get("birthday", None)
        # age_range = profile_response.get("age_range", None)
        gender = profile_response.get("gender", None)
        username = last_name + first_name  # korean
        # check user already exists
        if email is not None:
            user = models.User.objects.get_or_none(email=email)
        else:
            user = models.User.objects.get_or_none(username=username)
        if user is not None:
            if user.login_method != models.User.LOGIN_FACEBOOK:
                self.error_message = f"Please log in with: {user.login_method}"
                raise FacebookException(self.error_message)
        else:
            # create new user
            # check login by facebook user
            f_user = models.User.objects.get_or_none(
                username=f"facebook_name_{username}"
            )
            if f_user is not None:
                self.error_message = f"Facebook Login user already exists"
                raise FacebookException(self.error_message)

            user = models.User.objects.create(
                username=f"facebook_name_{username}",
                first_name=first_name,
                last_name=last_name,
                login_method=models.User.LOGIN_FACEBOOK,
                email=email if email is not None else f"facebook_{username}",
                gender=gender
                if gender is not None
                else models.User.GENDER_MALE,  # temporary
                email_verified=True,
            )
            login(request, user)
            return Response("Facebook Login Succeed!")


def login_google(request):
    """
    - reference
    https://developers.google.com/identity/protocols/OAuth2WebServer
    """
    client_id = os.environ.get("GOOGLE_ID")
    # scope : define the range of data received in the request
    # If want to use multiple scopes, use two spaces between scopes
    scope = "https://www.googleapis.com/auth/userinfo.email  https://www.googleapis.com/auth/userinfo.profile"
    redirect_uri = "https://127.0.0.1:8000/users/login/google/callback/"
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state=RANDOM&scope={scope}"
    )


class GoogleException(Exception):
    pass


class GoogleLoginCallback(mixins.LoginCallbackMixin, APIView):
    """
    - reference
    https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow
    """

    def __init__(self, *args, **kwargs):
        self.error_message = ""
        return super().__init__(*args, **kwargs)

    def get(self, request):
        try:
            access_token = self.get_access_token(request)
            profile_response = self.get_userinfo_from_access_token(access_token)
            response = self.check_user_and_login(request, profile_response)
            return response
        except GoogleException:
            return Response(self.error_message, status=status.HTTP_400_BAD_REQUEST)

    def get_access_token(self, request) -> str or Exception:
        client_id = os.environ.get("GOOGLE_ID")
        client_secret = os.environ.get("GOOGLE_SECRET")
        redirect_uri = "https://127.0.0.1:8000/users/login/google/callback/"
        code = request.GET.get("code", None)
        if code is None:
            self.error_message = "Can't get code info"
            raise GoogleException(self.error_message)
        api_url = f"https://oauth2.googleapis.com/token?code={code}&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&grant_type=authorization_code"
        result = requests.post(api_url)
        result_json = result.json()
        error = result_json.get("error", None)
        if error is not None:
            error_message = "Can't get access token"
            raise GoogleException(error_message)

        access_token = result_json.get("access_token")
        return access_token

    def get_userinfo_from_access_token(self, access_token: str):
        profile_url = (
            f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}"
        )
        profile_response = requests.get(profile_url).json()
        error = profile_response.get("error", None)
        if error is not None:
            error_message = "Can't get profile info"
            raise GoogleException(error_message)
        return profile_response

    def check_user_and_login(self, request, profile_response) -> Response:
        name = profile_response.get("name")
        email = profile_response.get("email")
        # check user already exists
        user = models.User.objects.get_or_none(email=email)
        if user is not None:
            if user.login_method != models.User.LOGIN_GOOGLE:
                error_message = f"Please log in with: {user.login_method}"
                raise GoogleException(error_message)
        else:
            # create new user
            user = models.User.objects.create(
                email=email,
                username=f"google_name_{name}",
                login_method=models.User.LOGIN_GOOGLE,
                gender=models.User.GENDER_FEMALE,  # temporary
                email_verified=True,
            )
        login(request, user)
        return Response("Google login Succeed!")


class MeView(RetrieveUpdateAPIView):
    """
    show or update login user's information API View Definition
    
    retrieve -> GET
    update -> PUT

    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        return self.retrieve(request)

    def retrieve(self, request):
        return Response(self.get_serializer(request.user).data)

    def put(self, request):
        return self.update(request)

    def update(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Update user data succeed!")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeFavsView(RetrieveUpdateAPIView):
    """
    show or update login user's favorites API View Definition

    retreive -> GET
    update -> PUT

    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserFavsSerializer

    def get(self, request):
        return self.retrieve(request)

    def retrieve(self, request):
        return Response(self.get_serializer(request.user).data)

    def put(self, request):
        return self.update(request)

    def update(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Update user favorites succeed!")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeReviewsView(ListAPIView):
    """
    retrieve login user's reviews API Definition

    create / retrieve / update / destory specific review 
    -> implemented in myapp.reviews.views (CreatedReviewAPIView, ProductReviewsAPIView)
    """

    permission_classes = [IsAuthenticated]
    serializer_class = MeReviewsSerializer
    queryset = review_models.Review.objects.all()
    paginator = BasicPagination()

    def get(self, request):
        return self.list(request)

    def list(self, request):
        qs = self.get_queryset()
        my_id = request.user.id
        my_reviews = qs.filter(user__id=my_id)
        page = self.paginate_queryset(my_reviews)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class MeScrapsView(RetrieveAPIView):
    """
    retrieve login user's API Definition

    retrieve : GET
    """

    permission_classes = [IsAuthenticated]
    serializer_class = MeScrapsSerializer

    def get(self, request):
        return self.retrieve(request)

    def retrieve(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MeSpecificScrapView(RetrieveDestroyAPIView):
    """
    retrieve, destroy my specific scrap API Definition

    retrieve -> GET
    destory -> DELETE
    """

    permission_classes = [IsAuthenticated]
    serializer_class = review_serializers.ReviewSerializer

    def get(self, request, review_id):
        return self.retrieve(request, review_id)

    def retrieve(self, request, review_id):
        my_reviews = request.user.scrap_reviews.all()
        for review in my_reviews:
            if review.id == review_id:
                serializer = self.get_serializer(review)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("review does not exists", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, review_id):
        return self.destroy(request, review_id)

    def destroy(self, request, review_id):
        my_reviews = request.user.scrap_reviews.all()
        for review in my_reviews:
            if review.id == review_id:
                request.user.scrap_reviews.remove(review)
                request.user.save()
                return Response("delete success", status=status.HTTP_200_OK)
        return Response("review does not exists", status=status.HTTP_404_NOT_FOUND)
