import os
from urllib import parse
import requests
import jwt
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from . import models


class SignUpAPIView(APIView):

    """ Sign up By Email API View Definition """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(UserSerializer(new_user).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    """ Log in By Email API View Definition """

    def get(self, request):
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


class LogoutAPIView(APIView):
    pass


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


@api_view(["GET"])
def naver_callback(request):
    error_message = ""
    try:
        client_id = os.environ.get("NAVER_ID")
        client_secret = os.environ.get("NAVER_SECRET")
        state = request.GET.get("state", None)
        redirect_uri = "https://127.0.0.1:8000/users/login/naver/callback/"
        code = request.GET.get("code", None)
        if code is None:
            error_message = "Can't get code info"
            raise NaverException(error_message)

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
            error_message = "Can't get access token"
            raise NaverException(error_message)
        # get naver profile (https://developers.naver.com/docs/login/profile/)
        access_token = result_json.get("access_token")
        header = "Bearer " + access_token
        url = "https://openapi.naver.com/v1/nid/me"
        profile_json = requests.get(url, headers={"Authorization": header}).json()
        profile_response = profile_json.get("response")
        if profile_response is not None:
            name = profile_response.get("name")
            email = profile_response.get("email")
            birthday = profile_response.get("birthday")
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
                    # birthdate="",
                )
            login(request, user)
            return Response("Naver login Succeed!")

    except NaverException:
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(["GET"])
def facebook_callback(request):
    """
    - reference
    https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow
    """
    error_message = ""
    try:
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
            error_message = "Can't get access token"
            raise FacebookException(message)

        # get access token(https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow)
        access_token = result_json.get("access_token")
        # get user id by using access token
        url = f"https://graph.facebook.com/debug_token?input_token={access_token}&access_token={access_token}"
        data = requests.get(url).json()
        user_id = data.get("data").get("user_id")
        # Finally, get profile data by using access_token and user_id
        # fields : https://developers.facebook.com/docs/graph-api/reference/user
        url = f"https://graph.facebook.com/v5.0/{user_id}?fields=email,first_name,last_name,birthday,age_range,gender&access_token={access_token}"
        profile_json = requests.get(url).json()
        error = profile_json.get("error")
        if error is not None:
            error_message = error.get("message")
            raise FacebookException(error_message)
        email = profile_json.get("email", None)
        first_name = profile_json.get("first_name", None)
        last_name = profile_json.get("last_name", None)
        birthday = profile_json.get("birthday", None)
        age_range = profile_json.get("age_range", None)
        gender = profile_json.get("gender", None)
        username = last_name + first_name  # korean
        # check user already exists
        if email is not None:
            user = models.User.objects.get_or_none(email=email)
        else:
            user = models.User.objects.get_or_none(username=username)
        if user is not None:
            if user.login_method != models.User.LOGIN_FACEBOOK:
                error_message = f"Please log in with: {user.login_method}"
                raise FacebookException(error_message)
        else:
            # create new user
            user = models.User.objects.create(
                username=f"facebook_name_{username}",
                first_name=first_name,
                last_name=last_name,
                login_method=models.User.LOGIN_FACEBOOK,
                email=email if email is not None else f"facebook_{username}",
                gender=gender
                if gender is not None
                else models.User.GENDER_MALE,  # temporary
            )
            login(request, user)
            return Response("Facebook Login Succeed!")

    except FacebookException:
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(["GET"])
def google_callback(request):
    error_message = ""
    try:
        client_id = os.environ.get("GOOGLE_ID")
        client_secret = os.environ.get("GOOGLE_SECRET")
        redirect_uri = "https://127.0.0.1:8000/users/login/google/callback/"
        code = request.GET.get("code", None)
        if code is None:
            error_message = "Can't get code info"
            raise GoogleException(error_message)

        api_url = f"https://oauth2.googleapis.com/token?code={code}&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&grant_type=authorization_code"
        result = requests.post(api_url)
        result_json = result.json()
        error = result_json.get("error", None)
        if error is not None:
            error_message = "Can't get access token"
            raise GoogleException(error_message)

        access_token = result_json.get("access_token")
        # id_token = result_json.get("id_token")
        # header = "Bearer " + access_token
        profile_url = (
            f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}"
        )
        profile_data = requests.get(profile_url)
        profile_json = profile_data.json()
        error = profile_json.get("error", None)
        if error is not None:
            error_message = "Can't get profile info"
            raise GoogleException(error_message)

        name = profile_json.get("name")
        email = profile_json.get("email")
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
            )
        login(request, user)
        return Response("Google login Succeed!")

    except GoogleException:
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

