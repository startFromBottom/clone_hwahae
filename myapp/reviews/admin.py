from django.contrib import admin
from django.utils.html import mark_safe
from . import models


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """ Review Admin """

    inlines = (PhotoInline,)

    list_display = (
        "good_review",
        "bad_review",
        "score",
        "user",
        "product",
        "num_favorites",
    )


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width=50px; src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
