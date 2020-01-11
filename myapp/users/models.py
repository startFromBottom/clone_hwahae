from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from myapp.core.models import SkinTypes
from django.utils.translation import gettext_lazy as _
from myapp.core import models as core_models
from myapp.core import managers as core_managers


class User(AbstractUser, core_models.TimeStampedModel):

    """ HWAHAE User Model """

    USERNAME_FIELD = "username"

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),  # (db, admin-form)
        (GENDER_FEMALE, "Female"),
    )

    SKINTYPE_CHOICES = (
        (SkinTypes.DRY, "Dry"),
        (SkinTypes.OILY, "Oily"),  # (db, admin-form)
        (SkinTypes.SENSITIVE, "Sensitive"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GOOGLE = "google"
    LOGIN_FACEBOOK = "facebook"
    LOGIN_NAVER = "naver"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GOOGLE, "Google"),
        (LOGIN_FACEBOOK, "Facebook"),
        (LOGIN_NAVER, "Naver"),
    )

    nickname = models.CharField(max_length=50)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=False,)
    skin_type = models.CharField(choices=SKINTYPE_CHOICES, max_length=10, blank=False,)
    birthdate = models.DateField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )
    point = models.IntegerField(default=0)
    favs_products = models.ManyToManyField("products.Product", related_name="users",)
    favs_ingredients = models.ManyToManyField(
        "products.Ingredient", related_name="users",
    )

    objects = core_managers.CustomBaseUserManager()
