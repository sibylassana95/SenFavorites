from django.db import models
from django.contrib.auth.models import User
from .utils.site_preview import get_site_preview

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    favicon_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.favicon_url:
            preview = get_site_preview(self.url)
            if preview['success']:
                self.favicon_url = preview['favicon_url']
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title