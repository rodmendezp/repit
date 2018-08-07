from rest_framework import serializers
from twitchdata.models import *


class TwitchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitchUser
        fields = ('twid', 'name',)


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('twid', )


class StreamerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streamer
        fields = ()


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
