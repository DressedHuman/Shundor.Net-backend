"""
Serializers for the Review model, handling input and display of product reviews.
"""
from rest_framework import serializers
from .models import Review
from product.models import Product
from user.models import User


class ReviewSerializer(serializers.ModelSerializer):
    # product_id and user_id are for input; product and user are for display
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )
    product = serializers.StringRelatedField(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user",
        write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "product", "product_id",
            "user", "user_id",
            "rating",
            "comment",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "user", "product"]


