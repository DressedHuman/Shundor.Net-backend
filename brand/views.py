from rest_framework import generics, permissions
from .models import Brand
from .serializers import BrandSerializer


# Anyone can view the list of brands
class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all().order_by('-id')
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]


# Only admins can create a new brand
class BrandCreateView(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]


# Only admins can update a brand by ID
class BrandUpdateView(generics.UpdateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


# Only admins can delete a brand by ID
class BrandDeleteView(generics.DestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

