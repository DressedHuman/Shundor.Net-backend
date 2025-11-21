

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import SiteSetting
from .serializers import SiteSettingSerializer



class SiteSettingListCreateAPIView(APIView):
    """
    API view to list all site settings (public) or create new settings (admin only).
    """

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request):
        settings = SiteSetting.objects.filter(status=True)
        serializer = SiteSettingSerializer(settings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SiteSettingSerializer(data=request.data)
        if serializer.is_valid():
            setting = serializer.save()
            return Response(SiteSettingSerializer(setting).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SiteSettingDetailAPIView(APIView):
    """
    API view to retrieve a site setting (public), update or delete (admin only).
    """

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_object(self, pk):
        return get_object_or_404(SiteSetting, pk=pk)

    def get(self, request, pk):
        setting = self.get_object(pk)
        serializer = SiteSettingSerializer(setting)
        return Response(serializer.data)

    def put(self, request, pk):
        setting = self.get_object(pk)
        serializer = SiteSettingSerializer(setting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        setting = self.get_object(pk)
        setting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
