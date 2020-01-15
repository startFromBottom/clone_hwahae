import os
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from abc import ABC, abstractmethod

from django.shortcuts import redirect, reverse, render
from django.contrib.auth import login
from django.db import Model
from myapp.users import models


class LoginCallback(ABC):
    """
    OAuth login callback methods defintions

    Each method must run sequentially in APIView's GET method.
    """

    @abstractmethod
    def get_access_token(self, request) -> str or Exception:
        """
        from the redirect url, get access token.
        Return access_token or exception
        """
        pass

    @abstractmethod
    def get_userinfo_from_access_token(self):
        """
        from access token, get user profile info.
        """
        pass

    @abstractmethod
    def check_user_and_login(self) -> Response:
        """
        check user info(Returned by get_userinfo_from_access_token) with
        databases, then return Response(200) or Response(400)
        """
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


class GoogleException(Exception):
    pass


class GoogleLoginCallback(APIView, LoginCallback):
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
            )
        login(request, user)
        return Response("Google login Succeed!")
