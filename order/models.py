from django.db import models
from user.models import User
from product.models import Product
from django.core.validators import MinValueValidator



class Order(models.Model):
    """
    Stores information about a customer's order, including status, user, and shipping details.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, db_index=True, blank=True, null=True
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    shipping_address = models.TextField()
    customer_name = models.CharField(max_length=100, blank=True, null=True)  # Name for guest checkout
    customer_phone = models.CharField(max_length=30, blank=True, null=True)  # Phone for guest checkout
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    customer_name_orderedby_admin = models.CharField(
        max_length=20, blank=True, null=True
    )
    customer_phone_orderedby_admin = models.CharField(
        max_length=20, blank=True, null=True
    )



class OrderItem(models.Model):
    """
    Represents a single product in an order, including quantity and price.
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, db_index=True, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, db_index=True
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)

