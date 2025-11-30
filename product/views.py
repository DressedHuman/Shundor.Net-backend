
"""
Views for managing products and product images, including creation, update, and retrieval endpoints.
"""




from rest_framework import generics, permissions
from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
import json






class ProductListView(generics.ListCreateAPIView):
    """
    List all products (public) or create a new product (admin only).
    """
    queryset = Product.objects.all().prefetch_related("images")
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
        "images", "reviews"
    )
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

def create_product_with_images(request):
    """
    Create a product with its images in a single request (admin only).
    Expects multipart form data with product fields and image files.
    """
    try:
        # Extract and validate product data
        product_data = {
            "name": request.data.get("name"),
            "slug": request.data.get("slug"),
            "category": request.data.get("category"),
            "brand": request.data.get("brand"),
            "description": request.data.get("description"),
            "sku": request.data.get("sku"),
            "price": request.data.get("price"),
            "old_price": request.data.get("old_price"),
            "stock": request.data.get("stock", 0),
            "is_active": request.data.get("is_active", "true").lower() == "true",
        }

        # Validate product data
        product_serializer = ProductSerializer(data=product_data)
        product_serializer.is_valid(raise_exception=True)
        product = product_serializer.save()

        # Process images
        images_json = request.data.get("images")
        if images_json:
            try:
                images_list = json.loads(images_json)

                for idx, image_data in enumerate(images_list):
                    # Get the image file for this image index
                    image_file = request.FILES.get(f"image_{idx}")
                    
                    if image_file:
                        # Create product image
                        ProductImage.objects.create(
                            product=product,
                            image=image_file,
                            alt_text=image_data.get("alt_text", ""),
                            is_primary=image_data.get("is_primary", idx == 0),
                            order=image_data.get("order", idx),
                        )

            except json.JSONDecodeError:
                return Response(
                    {"error": "Invalid JSON format in images field"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except KeyError as e:
                return Response(
                    {"error": f"Missing required field in image: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Return the complete product with images
        product_with_images = Product.objects.prefetch_related("images").get(
            id=product.id
        )
        return Response(
            ProductSerializer(product_with_images).data,
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        # Clean up if product was created but images failed
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


# ------------------- PRODUCT IMAGE VIEWS -------------------


# List all product images (GET)

class ProductImageListView(generics.ListAPIView):
    """
    List all product images (public).
    """
    queryset = ProductImage.objects.all().select_related("product")
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get"]


# Retrieve single image (GET)

class ProductImageDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single product image by its ID (public).
    """
    queryset = ProductImage.objects.all().select_related("product")
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get"]


# Update image (PUT/PATCH)

class ProductImageUpdateView(generics.UpdateAPIView):
    """
    Update an existing product image (authenticated users only).
    """
    queryset = ProductImage.objects.all().select_related("product")
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["put", "patch"]