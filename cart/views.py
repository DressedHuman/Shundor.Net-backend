
"""
Views for handling cart-related API requests.
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartView(generics.ListAPIView):
    """
    Get the current authenticated user's cart.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        return Cart.objects.filter(user=self.request.user)


class CartItemCreateView(generics.CreateAPIView):
    """
    Add an item to the cart (or update if exists).
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']

        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': serializer.validated_data['quantity']}
        )

        if not created:
            cart_item.quantity += serializer.validated_data['quantity']
            cart_item.save()

        serializer.instance = cart_item



class CartItemUpdateView(generics.UpdateAPIView):
    """
    Update quantity of a cart item.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class CartItemDeleteView(generics.DestroyAPIView):
    """
    Remove a cart item.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
