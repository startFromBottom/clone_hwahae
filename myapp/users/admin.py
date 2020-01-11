from django.contrib import admin
from . import models


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):

    """ Custom User Admin """

    list_display = (
        "email",
        "username",
        "gender",
        "point",
        "skin_type",
        "login_method",
    )

    list_filter = ("skin_type",)

    search_fields = ("=username",)
