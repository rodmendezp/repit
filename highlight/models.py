from django.db import models
from twitchdata.models import Video
from datetime import datetime


class Highlight(models.Model):
    video = models.ForeignKey(Video, on_delete=models.DO_NOTHING)
    start = models.TimeField()
    end = models.TimeField()
    created = models.DateTimeField(default=datetime.now)
    labeled = models.BooleanField(default=False)
