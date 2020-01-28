from myapp.core.error_collections import ErrorCollection
from rest_framework import status


AUTHENTICATION_ERROR_403 = ErrorCollection(
    code="not authenticated(403)",
    status=status.HTTP_403_FORBIDDEN,
    message="Authentication credentials were not provided.",
)

PRODUCTS_LIST_CONTAIN_INVALID_PARAM_400 = ErrorCollection(
    code="bad request(400)",
    status=status.HTTP_400_BAD_REQUEST,
    message="invalid query parameters. query parameters must be included in skin-type, category, include_ingredient, exclude_ingredient.",
)

PRODUCT_DETAIL_CONTAIN_INVALID_PARAM_400 = ErrorCollection(
    code="bad request(400)",
    status=status.HTTP_400_BAD_REQUEST,
    message="invalid query parameters. query parameters must be included in skin-type",
)

NOT_HAVE_SKIN_TYPE_PARAM_400 = ErrorCollection(
    code="bad request(400)",
    status=status.HTTP_400_BAD_REQUEST,
    message="request url must contain the skin_type parameter.",
)

INVALID_SKIN_TYPE_PARAM_400 = ErrorCollection(
    code="bad request(400)",
    status=status.HTTP_400_BAD_REQUEST,
    message="skin type must be one of dry, sensitive, oily.",
)
