import json

from datetime import datetime, time
from django.test import Client
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import status
from rest_framework.test import APITestCase
from twitchdata.models import *
from highlight.models import Highlight, Type


class HighlightRestAPITest(APITestCase):
    def setUp(self):
        self.user = self.create_user()
        self.twitch_user = self.create_twitch_user()
        self.channel = self.create_channel()
        self.streamer = self.create_streamer()
        self.game = self.create_game()
        self.video = self.create_video()
        self.type = self.create_type()
        self.highlight = self.create_highlight()
        self.baseURL = 'http://127.0.0.1:8000/'
        self.highlightAppURL = self.baseURL + 'highlight/'
        self.highlightURL = self.highlightAppURL + 'highlight/'
        self.typeURL = self.highlightAppURL + 'type/'
        self.client = Client()

    @staticmethod
    def create_user():
        user = get_user_model().objects.create(first_name='rodrigo', last_name='mendez', email='rodmendezp@gmail.com')
        user.set_password('rodrigomendez')
        user.save()
        return user

    @staticmethod
    def create_twitch_user():
        return TwitchUser.objects.create(twid=12345, name='raidrix')

    @staticmethod
    def create_channel():
        return Channel.objects.create(twid=1234)

    def create_streamer(self):
        return Streamer.objects.create(channel=self.channel, twitch_user=self.twitch_user)

    @staticmethod
    def create_game():
        return Game.objects.create(twid=123, name='PUBG')

    def create_video(self):
        return Video.objects.create(twid=12, streamer=self.streamer, game=self.game, recorded=datetime.now(), length=time(1, 35))

    @staticmethod
    def create_type():
        return Type.objects.create(name='Win')

    def create_highlight(self):
        return Highlight.objects.create(video=self.video, start=time(0, 12, 35), end=time(0, 13, 20))

    def test_put_highlight(self):
        credentials = {
            'email': 'rodmendezp@gmail.com',
            'password': 'rodrigomendez',
        }
        self.client.login(**credentials)
        pk = self.highlight.id
        data = {
            'type_id': self.type.id,
            'description': 'Highlight Description is Awesome',
            'start': time(0, 14, 20),
            'end': time(0, 15, 32),
        }
        response = self.client.put('/highlight/highlight/' + str(pk), json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_highlight = Highlight.objects.get(pk=pk)
        self.assertEqual(updated_highlight.id, self.highlight.id)
        self.assertEqual(updated_highlight.type.id, data['type_id'])
        self.assertEqual(updated_highlight.description, data['description'])
        self.assertEqual(updated_highlight.start, data['start'])
        self.assertEqual(updated_highlight.end, data['end'])
