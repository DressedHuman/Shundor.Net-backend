from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import ShippingCharge
from .serializers import ShippingChargeSerializer



class ShippingChargeListCreateAPIView(APIView):
    """
    API view to list all shipping charges (accessible to everyone) and create new charges (admin only).
    """

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request):
        charges = ShippingCharge.objects.all()
        serializer = ShippingChargeSerializer(charges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShippingChargeSerializer(data=request.data)
        if serializer.is_valid():
            charge = serializer.save()
            return Response(ShippingChargeSerializer(charge).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ShippingChargeDetailAPIView(APIView):
    """
    API view to retrieve a shipping charge (anyone), update or delete (admin only).
    """

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_object(self, pk):
        return get_object_or_404(ShippingCharge, pk=pk)

    def get(self, request, pk):
        charge = self.get_object(pk)
        serializer = ShippingChargeSerializer(charge)
        return Response(serializer.data)

    def put(self, request, pk):
        charge = self.get_object(pk)
        serializer = ShippingChargeSerializer(charge, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        charge = self.get_object(pk)
        charge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
