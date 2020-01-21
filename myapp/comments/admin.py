from django.contrib import admin
from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    """ Comment Admin Definition """

    list_display = (
        "content",
        "review",
        "comment_user",
    )
    pass
