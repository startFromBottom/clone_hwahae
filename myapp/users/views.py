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
    redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback/"
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
    try:
        client_id = os.environ.get("NAVER_ID")
        client_secret = os.environ.get("NAVER_SECRET")
        state = request.GET.get("state", None)
        redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback/"
        code = request.GET.get("code", None)
        if code is not None:
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
                raise NaverException("Can't get access token")
            else:
                # get naver profile (https://developers.naver.com/docs/login/profile/)
                access_token = result_json.get("access_token")
                header = "Bearer " + access_token
                url = "https://openapi.naver.com/v1/nid/me"
                profile_json = requests.get(
                    url, headers={"Authorization": header}
                ).json()
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
                            raise NaverException(
                                f"Please log in with: {user.login_method}"
                            )
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
                    return Response("Naver login succeed")

    except NaverException:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class LogoutAPIView(APIView):
    pass
