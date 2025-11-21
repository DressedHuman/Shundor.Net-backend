
from rest_framework import serializers
from .models import BlockedIP

# Used for blocking abusive or suspicious IPs
class BlockedIPSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlockedIP
		fields = ["id", "ip_address", "blocked_at", "reason"]
