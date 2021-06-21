from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.

class FeedUrl(TimeStampedModel):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.name


class FeedTag(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class FeedItem(TimeStampedModel):
    title = models.CharField(max_length=255)
    guid = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    url = models.URLField(max_length=255, null=True)
    tags = models.ManyToManyField(FeedTag)

    def __str__(self):
        return self.title
