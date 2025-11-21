from django.db import models

class Category(models.Model):
    """Product categories with hierarchical structure"""
    
    name = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    image= models.ImageField(upload_to='categories/', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name
    

    