from rest_framework import serializers
from .models import Review


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "good_review",
            "bad_review",
            "tip",
            "score",
        )


class ProductReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "good_review",
            "bad_review",
            "tip",
            "score",
            "user",
        )
