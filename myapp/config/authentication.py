import jwt
from django.conf import settings
from rest_framework import authentication
from myapp.users.models import User


class JWTAuthentication(authentication.BaseAuthentication):

    """
    custom jwt authentication definition class 

    When deploy to AWS elasticbeanstalk,
    should do WSGIPassAuthorization On
    https://www.django-rest-framework.org/api-guide/authentication/
    https://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/create-deploy-python-container.html
    """

    def authenticate(self, request):
        try:
            # if token not in request's Header -> not permitted
            token = request.META.get("HTTP_AUTHORIZATION")
            if token is None:
                return None
            xjwt, jwt_token = token.split(" ")
            decoded = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            pk = decoded.get("pk")
            user = User.objects.get(id=pk)
            return (user, None)
        except (ValueError, jwt.exceptions.DecodeError, User.DoesNotExist):
            return None
