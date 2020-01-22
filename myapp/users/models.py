import uuid
from datetime import datetime
from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from myapp.core.models import SkinTypes
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
    review_count = models.IntegerField(default=0)
    scrap_reviews = models.ManyToManyField("reviews.Review", related_name="users",)

    objects = core_managers.CustomBaseUserManager()

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                template_name="email/verify_email.html", context={"secret": secret}
            )
            send_mail(
                "Verify hwahae Account",  # subject
                strip_tags(html_message),  # html message
                settings.EMAIL_FROM,  # from
                [self.email],  # to
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return

    def favs_products_str(self):
        """
        convert id's list to string
        """
        names = [product.name for product in self.favs_products.all()]
        return ",".join(names)

    def favs_ingredients_str(self):
        """
        convert id's list to string
        """
        names = [ingredient.name for ingredient in self.favs_ingredients.all()]
        return ",".join(names)

    def get_age_range(self):
        pass

    def num_scraps(self):
        return len(self.scrap_reviews.all())

    def scrap_review_info(self):
        data = []
        for review in self.scrap_reviews.all():
            each = {
                "review_id": review.id,
                "review_user": {
                    "nickname": review.user.nickname,
                    "birthdate": review.user.birthdate,
                    "review_count": review.user.review_count,
                },
                "review_product": {
                    "name": review.product.name,
                    "imgUrl": review.product.imgUrl(),
                },
                "good_review": review.good_review,
                "bad_review": review.bad_review,
                "tip": review.tip,
                "score": review.score,
            }
            data.append(each)
        return data
