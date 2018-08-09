from rest_framework import serializers
from django.db import models
from twitchdata.models import *


# TODO: Support Create and Update for nested models

class TwitchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitchUser
        fields = ('id', 'twid', 'name')


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'twid')


class StreamerSerializer(serializers.ModelSerializer):
    twitch_user = TwitchUserSerializer()
    channel = ChannelSerializer()

    class Meta:
        model = Streamer
        fields = ('id', 'twitch_user', 'channel')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'twid', 'name')


class VideoSerializer(serializers.ModelSerializer):
    streamer = StreamerSerializer()
    game = GameSerializer()

    class Meta:
        model = Video
        fields = ('id', 'twid', 'streamer', 'game', 'recorded', 'length')


class ClipSerializer(serializers.ModelSerializer):
    streamer = StreamerSerializer()
    video = VideoSerializer()
    creator = TwitchUser()

    class Meta:
        model = Clip
        fields = ('id', 'streamer', 'video', 'creator', 'offset',
                  'duration', 'created', 'added', 'slug', 'title', 'views')


class EmoticonSerializer(serializers.ModelSerializer):
    streamer = StreamerSerializer()

    class Meta:
        model = Emoticon
        fields = ('id', 'twid', 'set_id', 'streamer', 'text')


class ChatSerializer(serializers.ModelSerializer):
    video = VideoSerializer()

    class Meta:
        model = Chat
        fields = ('id', 'video')


class MessageSerializer(serializers.ModelSerializer):
    chat = ChatSerializer()
    twitch_user = TwitchUserSerializer()

    class Meta:
        model = Message
        fields = ('id', 'chat', 'twitch_user', 'text', 'time')
