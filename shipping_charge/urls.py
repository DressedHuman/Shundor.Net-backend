

# API endpoints for shipping charges
from django.urls import path
from .views import ShippingChargeListCreateAPIView, ShippingChargeDetailAPIView

urlpatterns = [
	path('shipping-charges/', ShippingChargeListCreateAPIView.as_view(), name='shippingcharge-list-create'),
	path('shipping-charges/<int:pk>/', ShippingChargeDetailAPIView.as_view(), name='shippingcharge-detail'),
]
