from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from myapp.core import models as core_models
from myapp.core import managers as core_managers


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="review_photos")
    review = models.ForeignKey(
        "Review", related_name="photos", on_delete=models.CASCADE
    )


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    good_review = models.TextField(default="")
    bad_review = models.TextField(default="")
    tip = models.TextField(null=True)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    favorites = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "products.Product", related_name="reviews", on_delete=models.CASCADE
    )

    objects = core_managers.CustomModelManager()

    def __str__(self):
        return f"{self.product} - {self.user}"

    class Meta:
        ordering = ("-created",)
