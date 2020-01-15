from django.db import models
from myapp.core import models as core_models


class Comment(core_models.TimeStampedModel):

    """ Comment Model Definition """

    content = models.TextField()
    comment_user = models.ForeignKey(
        "users.User", related_name="comments", on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        "reviews.Review", related_name="comments", on_delete=models.CASCADE
    )
