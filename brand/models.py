from django.db import models

class Brand(models.Model):
    """Product brands"""
   
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    brand_img= models.ImageField(upload_to='brands/', null=True, blank=True)
    
    def __str__(self):
        return self.name