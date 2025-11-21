
"""
Views for managing FraudAPI objects.
Only admin users are allowed to access these endpoints.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import FraudAPI
from .serializers import FraudAPISerializer


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to allow access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class FraudAPIListCreateView(APIView):
    """
    List all FraudAPI entries or create a new one.
    Only accessible by admin users.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        """Return a list of all FraudAPI objects, ordered by creation date."""
        fraud_apis = FraudAPI.objects.all().order_by("-created_at")
        serializer = FraudAPISerializer(fraud_apis, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new FraudAPI object from the provided data."""
        serializer = FraudAPISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FraudAPIDetailView(APIView):
    """
    Retrieve, update, or delete a specific FraudAPI object by ID.
    Only accessible by admin users.
    """
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        """Helper to get a FraudAPI object or return 404 if not found."""
        return get_object_or_404(FraudAPI, pk=pk)

    def get(self, request, pk):
        """Retrieve a FraudAPI object by its primary key."""
        fraud_api = self.get_object(pk)
        serializer = FraudAPISerializer(fraud_api)
        return Response(serializer.data)

    def put(self, request, pk):
        """Update a FraudAPI object with the provided data."""
        fraud_api = self.get_object(pk)
        serializer = FraudAPISerializer(fraud_api, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Partially update a FraudAPI object."""
        fraud_api = self.get_object(pk)
        serializer = FraudAPISerializer(fraud_api, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a FraudAPI object."""
        fraud_api = self.get_object(pk)
        fraud_api.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
