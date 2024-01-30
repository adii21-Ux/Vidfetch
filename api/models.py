from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField(blank=True, null=True)
    channel_id = models.CharField(max_length=50, blank=True)
    channel_title = models.CharField(max_length=100, blank=True)
    thumbnail_medium_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
