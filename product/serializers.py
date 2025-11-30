"""
Serializers for the Product and ProductImage models, including nested and related data for API responses.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, ProductImage, Category, Brand, Size, Color
from review.models import Review


User = get_user_model()




class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, nested inside Review serializer.
    """
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name"]  # Include other fields if needed

    def get_name(self, obj):
        """
        Combine first_name and last_name from user's profile into a full name.
        """
        if hasattr(obj, 'profile') and obj.profile:
            first_name = obj.profile.first_name or ''
            last_name = obj.profile.last_name or ''
            return f"{first_name} {last_name}".strip()
        return ""  # Return empty string if no profile exists


class ReviewTobeIncludedInProductSerializer(serializers.ModelSerializer):
    """
    Serializer for including reviews in product detail response.
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "rating",
            "comment",
            "created_at",
        ]


class SizeSerializer(serializers.ModelSerializer):
    """Serializer for Size model."""
    class Meta:
        model = Size
        fields = ['id', 'name', 'code', 'order', 'is_active']
        read_only_fields = ['id']


class ColorSerializer(serializers.ModelSerializer):
    """Serializer for Color model."""
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code', 'is_active']
        read_only_fields = ['id']


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images."""
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product with images, sizes, colors, and reviews."""
    images = ProductImageSerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    size_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Size.objects.all(), 
        source='sizes', 
        write_only=True,
        required=False
    )
    color_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Color.objects.all(), 
        source='colors', 
        write_only=True,
        required=False
    )
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    reviews = ReviewTobeIncludedInProductSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'category_name', 'brand', 'brand_name', 
            'description', 'sku', 'old_price', 'price', 'stock', 'is_active', 
            'created_at', 'updated_at', 'images', 'sizes', 'colors', 
            'size_ids', 'color_ids', 'reviews'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

