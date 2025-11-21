from django.db import models
from user.models import User
from product.models import Product

class Wishlist(models.Model):
    """
    Stores products a user has added to their wishlist.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    
    class Meta:
        unique_together = ['user', 'product']
    
    def __str__(self):
        # Show which user and product this wishlist entry is for
        return f"{self.user.email if self.user else 'Guest'} - {self.product.name}"
    

    