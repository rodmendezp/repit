from django.db import models
from twitchdata.models import Video
from backend.models import User
from datetime import datetime


class Type(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='children', blank=True, null=True)


class Highlight(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=255, default='')
    start = models.TimeField()
    end = models.TimeField()
    created = models.DateTimeField(default=datetime.now)
    labeled = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
