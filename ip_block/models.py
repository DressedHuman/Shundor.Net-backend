
from django.db import models


class BlockedIP(models.Model):
    """
    Model for storing blocked IP addresses and the reason for blocking.
    """
    id = models.AutoField(primary_key=True)
    ip_number = models.GenericIPAddressField()
    reason = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the blocked IP and reason.
        """
        return f"{self.ip_number} - {self.reason[:50]}"


