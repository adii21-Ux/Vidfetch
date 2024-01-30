from django.db import models

# Create your models here.
from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=50)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    published_at = models.DateTimeField()
    channel_id = models.CharField(max_length=50)
    channel_title = models.CharField(max_length=100)
    thumbnail_medium_url = models.URLField()

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
