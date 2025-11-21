from django.db import models

class Banner(models.Model):
    image = models.ImageField(upload_to="banners/", blank=False, null=False)
    url = models.CharField(max_length=2083)
    label = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)