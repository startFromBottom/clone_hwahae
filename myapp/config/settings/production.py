import os
from .base import *

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "HOST": os.environ["MYSQL_ROOT_HOST"],
#         "NAME": os.environ["MYSQL_DATABASE"],
#         "USER": os.environ["MYSQL_USER"],
#         "PASSWORD": os.environ["MYSQL_ROOT_PASSWORD"],
#         "PORT": "3306",
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "NAME": "cosmetic_db",
        "USER": "programmer",
        "PASSWORD": "1234",
        "PORT": "3306",
        "OPTIONS": {"charset": "utf8mb4"},
        "TEST": {"NAME": "test_cosmetic_db",},
    }
}
