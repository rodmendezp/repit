from django.db import models
from django.utils import timezone


class TwitchModel(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    twid = models.IntegerField(unique=True)

    class Meta:
        abstract = True


class TwitchUser(TwitchModel):
    name = models.CharField(unique=True, max_length=100)


class Channel(TwitchModel):
    pass


class Streamer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    twitch_user = models.ForeignKey(TwitchUser, on_delete=models.DO_NOTHING)
    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING)


class Game(TwitchModel):
    name = models.CharField(unique=True, max_length=255)


class Video(TwitchModel):
    streamer = models.ForeignKey(Streamer, on_delete=models.DO_NOTHING)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    recorded = models.DateTimeField()
    length = models.TimeField()


class Clip(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    streamer = models.ForeignKey(Streamer, on_delete=models.DO_NOTHING)
    video = models.ForeignKey(Video, on_delete=models.DO_NOTHING)
    creator = models.ForeignKey(TwitchUser, on_delete=models.DO_NOTHING)
    offset = models.TimeField()
    duration = models.TimeField()
    created = models.DateTimeField()
    added = models.DateTimeField(default=timezone.now)
    slug = models.CharField(unique=True, max_length=50)
    title = models.TextField()
    views = models.IntegerField()


class Emoticon(TwitchModel):
    set_id = models.IntegerField(default=0)
    streamer = models.ForeignKey(Streamer, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=100)


class Chat(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.DO_NOTHING)

    @property
    def filename(self):
        return 'v' + str(self.video.twid) + '.txt'


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.DO_NOTHING)
    twitch_user = models.ForeignKey(TwitchUser, on_delete=models.DO_NOTHING)
    text = models.TextField()
    time = models.TimeField()
