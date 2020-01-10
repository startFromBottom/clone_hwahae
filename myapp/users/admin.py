from django.contrib import admin
from . import models


@admin.register(models.HwaHaeUser)
class CustomUserAdmin(admin.ModelAdmin):

    """ Custom User Admin """

    list_display = (
        "email",
        "username",
        "gender",
        "point",
        "skin_type",
        "login_method",
        "superuser",
    )

    list_filter = (
        "skin_type",
        "superuser",
    )

    search_fields = ("=username",)
