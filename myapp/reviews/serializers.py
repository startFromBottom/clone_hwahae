from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "good_review",
            "bad_review",
            "tip",
            "score",
            "user",
        )
        read_only_fields = ("user",)
