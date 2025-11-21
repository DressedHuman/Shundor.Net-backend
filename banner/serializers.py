from rest_framework import serializers
from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Banner
        fields = (
            "id",
            "image",
            "url",
            "label",
            "is_active",
            "created_at",
            "modified_at",
        )
        # All fields are included for full banner details
