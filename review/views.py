"""
Views for managing product reviews, including listing, updating, and status changes.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import Review
from .serializers import ReviewSerializer



class ReviewAPIView(APIView):
    """
    List, retrieve, update, or delete reviews.
    Admins can manage all reviews; users can view their own.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        if pk:  # Single review
            review = get_object_or_404(
                Review.objects.select_related("user", "product"), pk=pk
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)

        # List reviews
        if request.user.is_staff:
            reviews = Review.objects.all().select_related("user", "product")
        else:
            reviews = Review.objects.filter(user=request.user).select_related("product")

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if not request.user.is_staff:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        
        if not request.user.is_staff:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

           
            
            return Response({"msg": "successfully updated"})
            

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not request.user.is_staff:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        review = get_object_or_404(Review, pk=pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ReviewStatusUpdateAPIView(APIView):
    """
    Admins can update review status (publish/pending).
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        status_value = request.data.get("status")
        if status_value not in dict(Review.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        review.status = status_value
        review.save()
        return Response({"status": review.status})
