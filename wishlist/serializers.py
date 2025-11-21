"""
Serializers for the Wishlist model, handling input and display of wishlist entries.
"""
from rest_framework import serializers
from .models import Wishlist
from product.models import Product
from user.models import User


class WishlistSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user",
        write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "user", "user_id", "product", "product_id"]
        read_only_fields = ["id", "user", "product"]
