from abc import ABC, abstractmethod
from rest_framework.response import Response


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
