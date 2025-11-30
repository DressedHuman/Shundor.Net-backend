from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.shortcuts import get_object_or_404

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer



class OrderListCreateAPIView(APIView):
    """
    List all orders (admin only) or create a new order (anyone).
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if not request.user.is_staff:  # or request.user.is_superuser
            return Response(
                {"detail": "Only admins can view all orders."},
                status=status.HTTP_403_FORBIDDEN,
            )
        orders = Order.objects.all().order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        # Allow unauthenticated users to create orders (guest checkout).
        # Do not force-insert `user` into the request data; instead pass
        # request.user to serializer.save() so the serializer can decide
        # whether to attach a user or leave it NULL for guest orders.

        serializer = OrderSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            save_kwargs = {
                "customer_name_orderedby_admin": data.get(
                    "customer_name_orderedby_admin"
                ),
                "customer_phone_orderedby_admin": data.get(
                    "customer_phone_orderedby_admin"
                ),
            }

            # Only pass a User instance if the request is authenticated
            save_kwargs["user"] = request.user if request.user.is_authenticated else None

            order = serializer.save(**save_kwargs)
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderDetailAPIView(APIView):
    """
    Retrieve, update, or delete a specific order.
    Admins can access any order; users can only access their own.
    """

    permission_classes = [permissions.IsAuthenticated]  # Removed IsAdminUser from here

    def get_object(self, pk, user):
        if user.is_staff:
            # Admins can access any order (don't filter by user)
            return get_object_or_404(
                Order.objects.prefetch_related("items__product"), pk=pk
            )
        else:
            # Regular users can only access their own orders
            return get_object_or_404(
                Order.objects.prefetch_related("items__product"),
                pk=pk,
                user=user,
            )

    def get(self, request, pk):
        order = self.get_object(pk, request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        # Only allow admins to update orders
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admins can update orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        order = self.get_object(pk, request.user)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Only allow admins to delete orders
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admins can delete orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        order = self.get_object(pk, request.user)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class OrderStatusUpdateAPIView(APIView):
    """
    Update only the status of an order (admins only).
    """

    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        status_value = request.data.get("status")

        if status_value not in dict(Order.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status_value
        order.save()
        return Response({"status": order.status})



class OrderItemListCreateAPIView(APIView):
    """
    List all order items or create a new one (admin only).
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        items = OrderItem.objects.filter(order__user=request.user).select_related(
            "order", "product"
        )
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            return Response(
                OrderItemSerializer(item).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderItemDetailAPIView(APIView):
    """
    Retrieve, update, or delete a specific order item (admin only).
    """

    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_object(self, pk, user):
        return get_object_or_404(
            OrderItem.objects.select_related("order", "product"),
            pk=pk,
            order__user=user,
        )

    def get(self, request, pk):
        item = self.get_object(pk, request.user)
        serializer = OrderItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk, request.user)
        serializer = OrderItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk, request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class OrderHistoryView(generics.ListAPIView):
    """
    Shows the order history for the current user (newest first).
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")
