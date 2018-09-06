from rest_framework.test import APITestCase
from twitchdata.models import *
from highlight.models import *
from datetime import datetime, time


class HighlightRestAPITest(APITestCase):
    def setUp(self):
        super().setUp()

    def test_update_highlight(self):
        pass

    def add_video(self):
        twitch_user = TwitchUser.objects.create(twid=12345, name='raidrix')
        channel = Channel.objects.create(twid=1234)
        streamer = Streamer.objects.create(twitch_user=twitch_user, channel=channel)
        game = Game.objects.create(twid=123, name='PUBG')
        try:
            user = User.objects.get(pk=1)
        except User.DoesNotExist:
            user = User.objects.create(first_name='rodrigo', last_name='mendez', emial='rodmendezp@gmail.com')
        video = Video.objects.create(twid=12, streamer=streamer, game=game, recorded=datetime.now(), length=time(1, 35))
        return video

