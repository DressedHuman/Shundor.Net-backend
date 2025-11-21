# fraud/serializers.py
from rest_framework import serializers
from .models import FraudAPI

class FraudAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudAPI
        fields = ["id", "type", "api_url", "api_key", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]  # IDs and timestamps are read-only
