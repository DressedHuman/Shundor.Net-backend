from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "hotline_number",
            "email",
            "phone_number",
            "whatsapp_number",
            "address",
            "google_map",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]  # Timestamps are set automatically
