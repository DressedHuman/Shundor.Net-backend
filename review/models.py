from django.db import models
from product.models import Product
from user.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    """
    Stores a user's review for a product, including rating, comment, and status.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('published', 'Published'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        db_index=True
    )
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
   