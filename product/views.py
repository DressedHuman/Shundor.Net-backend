
"""
Views for managing products and product variants, including creation, update, and retrieval endpoints.
"""




from rest_framework import generics, permissions
from .models import Product, ProductVariant
from .serializers import ProductSerializer, ProductVariantSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
import json






class ProductListView(generics.ListCreateAPIView):
    """
    List all products (public) or create a new product (admin only).
    """
    queryset = Product.objects.all().prefetch_related("variants")
    serializer_class = ProductSerializer
    http_method_names = ["get", "post"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        elif self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return super().get_permissions()



class ProductDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single product by its ID (public).
    """

    # Prefetch related objects to optimize database queries.
    queryset = Product.objects.filter(is_active=True).prefetch_related(
        "variants"
    )  # , 'reviews__user')
    serializer_class = ProductSerializer
    lookup_field = "id"


# Create product (POST)

class ProductCreateView(generics.CreateAPIView):
    """
    Create a new product (authenticated users only).
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])

def create_product_with_variants(request):
    """
    Create a product with its variants in a single request (admin only).
    Expects multipart form data with product fields and a JSON list of variants.
    """
    try:
        # Extract and validate product data
        product_data = {
            "name": request.data.get("name"),
            "slug": request.data.get("slug"),
            "category": request.data.get("category"),
            "brand": request.data.get("brand"),
            "description": request.data.get("description"),
            "is_active": request.data.get("is_active", "true").lower() == "true",
        }

        # Validate product data
        product_serializer = ProductSerializer(data=product_data)
        product_serializer.is_valid(raise_exception=True)
        product = product_serializer.save()

        # Process variants
        variants_json = request.data.get("variants")
        if variants_json:
            try:
                variants_list = json.loads(variants_json)

                for idx, variant_data in enumerate(variants_list):
                    # Get the image file for this variant index
                    image_file = request.FILES.get(f"variant_image_{idx}")

                    # Create variant directly using the model instead of serializer
                    # to avoid the product_id field validation issue
                    ProductVariant.objects.create(
                        product=product,  # Pass the product instance, not ID
                        sku=variant_data.get("sku"),
                        price=variant_data.get("price"),
                        old_price=variant_data.get("old_price"),
                        stock=variant_data.get("stock"),
                        color=variant_data.get("color"),
                        size=variant_data.get("size"),
                        is_active=variant_data.get("is_active", True),
                        image=image_file,
                    )

            except json.JSONDecodeError:
                return Response(
                    {"error": "Invalid JSON format in variants field"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except KeyError as e:
                return Response(
                    {"error": f"Missing required field in variant: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Return the complete product with variants
        product_with_variants = Product.objects.prefetch_related("variants").get(
            id=product.id
        )
        return Response(
            ProductSerializer(product_with_variants).data,
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        # Clean up if product was created but variants failed
        if "product" in locals():
            product.delete()

        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Update product (PUT/PATCH)

class ProductUpdateView(generics.UpdateAPIView):
    """
    Update an existing product (authenticated users only).
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"
    http_method_names = ["put", "patch"]


# ------------------- PRODUCT VARIANT VIEWS -------------------


# List all product variants (GET)

class ProductVariantListView(generics.ListAPIView):
    """
    List all product variants (public).
    """
    queryset = ProductVariant.objects.all().select_related("product")
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get"]


# Retrieve single variant (GET)

class ProductVariantDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single product variant by its ID (public).
    """
    queryset = ProductVariant.objects.all().select_related("product")
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get"]


# Update variant (PUT/PATCH)

class ProductVariantUpdateView(generics.UpdateAPIView):
    """
    Update an existing product variant (authenticated users only).
    """
    queryset = ProductVariant.objects.all().select_related("product")
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["put", "patch"]