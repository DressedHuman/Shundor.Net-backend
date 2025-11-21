
from django.db import models


class ShippingCharge(models.Model):
    """
    Model for storing shipping charges by area.
    """
    area = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the shipping charge for the area.
        """
        return f"{self.area} - ${self.amount}"
