from django.http import QueryDict
from rest_framework.response import Response
from rest_framework import status
from myapp.core.models import SkinTypes


SKIN_TYPE_PARAM = "skin_type"


class APIParams:
    products_list_params = (
        SKIN_TYPE_PARAM,
        "category",
        "page",
        "exclude_ingredient",
        "include_ingredient",
    )

    product_detail_params = (SKIN_TYPE_PARAM,)


class ParamsCheck:
    """
    check if query params are validated.
    all exceptions related with query params are handled in
    this class
    """

    @classmethod
    def _contain_invalid_param(cls, query_params: QueryDict, possible_params: tuple):
        """
        if True -> raise exception -> return 404 response in other method
        """
        for param in query_params.keys():
            if param not in possible_params:
                raise InvalidParamsException()
        return None

    @classmethod
    def _have_skin_type_param(cls, query_params: QueryDict, possible_params: tuple):
        """
        if False -> raise exception -> return 400 response in other method
        """
        for param in query_params.keys():
            if param == SKIN_TYPE_PARAM:
                return None
        raise NotContainSkinTypeException()

    @classmethod
    def _valid_skin_type(cls, query_params: QueryDict):
        """
        if False -> raise exception -> return 400 response in other method
        """
        value = query_params.get(SKIN_TYPE_PARAM)
        if value not in [SkinTypes.DRY, SkinTypes.OILY, SkinTypes.SENSITIVE]:
            raise InvalidSkinTypeException()
        return None

    @classmethod
    def validate(cls, query_params: QueryDict, possible_params: tuple):
        try:
            cls._contain_invalid_param(query_params, possible_params)
            cls._have_skin_type_param(query_params, possible_params)
            cls._valid_skin_type(query_params)
        except InvalidParamsException:
            string = ", ".join(possible_params)
            return Response(
                f"invalid query parameters. query parameters must be included in {string}",
                status=status.HTTP_400_BAD_REQUEST,
            )
        except NotContainSkinTypeException:
            return Response(
                "Request url must contain the skin_type parameter",
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSkinTypeException:
            return Response(
                "skin type must be one of dry, sensitive, oily",
                status=status.HTTP_400_BAD_REQUEST,
            )
        return False


class InvalidParamsException(Exception):
    pass


class NotContainSkinTypeException(Exception):
    pass


class InvalidSkinTypeException(Exception):
    pass
