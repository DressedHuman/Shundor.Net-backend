
from django.db import models


class SiteSetting(models.Model):
    """
    Model for storing site-wide settings such as logos and status.
    """
    site_name = models.CharField(max_length=255)
    white_logo = models.ImageField(upload_to='logos/white/')
    dark_logo = models.ImageField(upload_to='logos/dark/')
    favicon = models.ImageField(upload_to='favicons/')
    status = models.BooleanField(default=True)

    def __str__(self):
        """
        Returns the site name for this setting.
        """
        return self.site_name
