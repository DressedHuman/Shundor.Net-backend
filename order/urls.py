"""
URL patterns for the order app.
Routes for order and order item endpoints.
"""
from django.urls import path
from .views import (
    OrderListCreateAPIView,
    OrderDetailAPIView,
    OrderStatusUpdateAPIView,
    OrderItemListCreateAPIView,
    OrderItemDetailAPIView,
    OrderHistoryView
)

urlpatterns = [
    # Orders
    path("orders/", OrderListCreateAPIView.as_view(), name="order-list-create"),
    path("orders/<int:pk>/", OrderDetailAPIView.as_view(), name="order-detail"),
    path("orders/<int:pk>/update-status/", OrderStatusUpdateAPIView.as_view(), name="order-status-update"),

    # Order Items
    path("order-items/", OrderItemListCreateAPIView.as_view(), name="orderitem-list-create"),
    path("order-items/<int:pk>/", OrderItemDetailAPIView.as_view(), name="orderitem-detail"),

    path("order-history/", OrderHistoryView.as_view(), name="order-history"),
]








