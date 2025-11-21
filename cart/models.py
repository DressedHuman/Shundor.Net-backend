from django.db import models
from user.models import User
from product.models import ProductVariant
from django.core.validators import MinValueValidator


class Cart(models.Model):
    # Represents a user's shopping cart

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        # Show cart owner for admin/debug
        return f"Cart - {self.user.email if self.user else 'Guest'}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="cart_item",
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    class Meta:
        unique_together = ["cart", "product_variant"]

