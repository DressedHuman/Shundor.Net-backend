from django.db import models
from category.models import Category
from brand.models import Brand
from django.core.validators import MinValueValidator

class Product(models.Model):
    """
    Main product model representing a sellable item.
    """
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_index=True)
    description = models.TextField()
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)], default=0)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    
    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    Model to store multiple images for a product.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"

    





