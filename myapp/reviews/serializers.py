from rest_framework import serializers
from .models import Review, Photo


class ReviewSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source="user.username")
    skin_type = serializers.ReadOnlyField(source="user.skin_type")
    birthdate = serializers.ReadOnlyField(source="user.birthdate")
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = Review
        fields = (
            "product_name",
            "username",
            "good_review",
            "bad_review",
            "tip",
            "score",
            "skin_type",
            "birthdate",
            "photo_urls",
        )


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.ImageField()
    review = serializers.ReadOnlyField(source="review.__str__")

    class Meta:
        model = Photo
        fields = (
            "review",
            "caption",
            "file",
        )
