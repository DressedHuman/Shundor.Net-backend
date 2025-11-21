
from rest_framework import serializers
from .models import SiteSetting

# For managing key-value site settings
class SiteSettingSerializer(serializers.ModelSerializer):
	class Meta:
		model = SiteSetting
		fields = ["id", "key", "value", "updated_at"]
