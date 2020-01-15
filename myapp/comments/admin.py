from django.contrib import admin
from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    """ Comment Admin Definition """

    # list_display = (
    #     "review",
    #     "comment_user",
    #     "content",
    # )
    pass
