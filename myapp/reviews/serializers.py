from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source="user.username")
    skin_type = serializers.ReadOnlyField(source="user.skin_type")
    birthdate = serializers.ReadOnlyField(source="user.birthdate")

    class Meta:
        model = Review
        fields = (
            "good_review",
            "bad_review",
            "tip",
            "score",
            "username",
            "skin_type",
            "birthdate",
        )
