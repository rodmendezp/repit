from rest_framework import serializers
from django.db import models
from twitchdata.models import *


# TODO: Support Create and Update for nested models

class TwitchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitchUser
        fields = ('twid', 'name',)


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('twid', )


class StreamerSerializer(serializers.ModelSerializer):
    twitch_user = TwitchUserSerializer()
    channel = ChannelSerializer()

    def create(self, validated_data):
        twitch_user_data = validated_data.pop('twitch_user')
        twitch_user = TwitchUser.objects.create(**twitch_user_data)
        channel_data = validated_data.pop('channel')
        channel = Channel.objects.create(**channel_data)
        streamer = Streamer.objects.create(twitch_user=twitch_user, channel=channel)
        return streamer

    def update(self, instance, validated_data):
        twitch_user_data = validated_data.get('twitch_user', None)
        twitch_user_id = twitch_user_data.get('id', None)
        if twitch_user_id:
            try:
                twitch_user = TwitchUser.objects.get(pk=twitch_user_id)
            except models.ObjectDoesNotExist:
                return
        channel_data = validated_data.get('channel', None)
        channel_id = channel_data.get('id', None)
        if channel_id:
            try:
                channel = Channel.objects.get(pk=channel_id)
            except models.ObjectDoesNotExist:
                return
        streamer = instance
        if twitch_user:
            streamer.twitch_user = twitch_user
        if channel:
            streamer.channel = channel
        streamer.save()
        return streamer

    class Meta:
        model = Streamer
        fields = ('twitch_user', 'channel')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('twid', 'name', )


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('twid', 'recorded', 'length')


class ClipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clip
        fields = ('twid', 'title', 'views')


class EmoticonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoticon
        fields = ('set_id', 'text')


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', 'time')
