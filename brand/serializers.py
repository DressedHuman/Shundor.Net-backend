from rest_framework import serializers
from .models import Brand

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "slug",
            "created_at",
            "brand_img"
        ]
        read_only_fields = ["created_at"]  # created_at is set automatically

