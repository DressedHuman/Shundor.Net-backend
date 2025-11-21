
# Create your models here.
from django.db import models


class FraudAPI(models.Model):
    """
    Model representing a third-party fraud detection API configuration.
    """
    API_TYPE_CHOICES = [
        ('ip', 'IP Fraud Detection'),
        ('email', 'Email Fraud Detection'),
        ('phone', 'Phone Fraud Detection'),
        ('custom', 'Custom API'),
    ]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=API_TYPE_CHOICES)
    api_url = models.URLField()
    api_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the FraudAPI instance.
        """
        return f"{self.get_type_display()} API - {self.api_url}"



