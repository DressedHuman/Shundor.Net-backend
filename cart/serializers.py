from rest_framework import serializers
from .models import Cart, CartItem
from product.serializers import ProductSerializer



class CartItemSerializer(serializers.ModelSerializer):
    # product is for display, product_id is for input
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=CartItem._meta.get_field('product').related_model.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_id",
            "quantity",
        ]


class CartSerializer(serializers.ModelSerializer):
    # items is a list of CartItemSerializer objects
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "created_at",
            "items",
        ]
        read_only_fields = ["id", "created_at"]





