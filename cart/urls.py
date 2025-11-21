from django.urls import path
from .views import CartView, CartItemCreateView, CartItemUpdateView, CartItemDeleteView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart-detail"),
    path("items/", CartItemCreateView.as_view(), name="cartitem-create"),
    path("items/<str:id>/", CartItemUpdateView.as_view(), name="cartitem-update"),
    path("items/<str:id>/delete/", CartItemDeleteView.as_view(), name="cartitem-delete"),
]


