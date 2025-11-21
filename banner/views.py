from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Banner
from .serializers import BannerSerializer


# Return all banners (admin or public)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_banners(req):
    banners = Banner.objects.all()
    serializer = BannerSerializer(banners, many=True, context={"request": req})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


# Return only banners that are currently active
@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_active_banners(req):
    banners = Banner.objects.filter(is_active=True)
    serializer = BannerSerializer(banners, many=True, context={"request": req})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


# Add a new banner
@api_view(["POST"])
@permission_classes([AllowAny])
def add_banner(req):
    serializer = BannerSerializer(data=req.data, context={"request": req})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update an existing banner by ID
@api_view(["PUT"])
@permission_classes([AllowAny])
def update_banner(req, pk):
    target_banner = get_object_or_404(Banner, id=pk)
    serializer = BannerSerializer(target_banner, data=req.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Change the publish status (active/inactive) of a banner
@api_view(["PATCH"])
@permission_classes([AllowAny])
def update_banner_publish_status(req, pk):
    target_banner = get_object_or_404(Banner, id=pk)
    is_active = req.data.get("is_active")
    if is_active is None:
        return Response(
            {"error": "is_active field is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    target_banner.is_active = is_active
    target_banner.save()
    return Response(
        {"message": "status updated successfully."}, status=status.HTTP_200_OK
    )


# Delete a banner by ID
@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_banner(req, pk):
    target_banner = get_object_or_404(Banner, id=pk)
    target_banner.delete()
    return Response(
        {"message": "Banner deleted successfully."}, status=status.HTTP_204_NO_CONTENT
    )
