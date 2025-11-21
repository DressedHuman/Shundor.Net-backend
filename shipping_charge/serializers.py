
from rest_framework import serializers
from .models import ShippingCharge

# Used for displaying and updating shipping charges by region
class ShippingChargeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShippingCharge
		fields = ["id", "region", "charge", "created_at", "updated_at"]
