import collections

from rest_framework import serializers
from twitchdata.models import *


# TODO: Support Create and Update for nested models

class ModelSupportNestedSerializer(serializers.ModelSerializer):
    def get_by_id(self, data):
        instance = self.Meta.model.objects.get(pk=data.get('id'))
        instance_dict = instance.__dict__
        for key, value in instance_dict.items():
            if '_id' in key:
                instance_dict[key.replace('_id', '')] = instance_dict.pop(key)
        for key, value in data.items():
            if key in instance_dict:
                instance_dict[key] = value
        return collections.OrderedDict(instance_dict)

    def to_internal_value_nested(self, data):
        if data.get('id', None) is None:
            return super(ModelSupportNestedSerializer, self).to_internal_value(data)
        return self.get_by_id(data)

    def to_internal_value(self, data):
        return self.to_internal_value_nested(data)

    def deep_create(self, validated_data, nested_serializer):
        validated_data = dict(validated_data)
        nested_objects = {}
        for field in nested_serializer._writable_fields:
            if isinstance(field, serializers.BaseSerializer):
                if any(isinstance(field, serializers.BaseSerializer) for field in field._writable_fields):
                    nested_objects[field.source] = self.deep_create(validated_data.pop(field.source), field)
                else:
                    nested_objects[field.source] = field.Meta.model.objects.create(**validated_data.pop(field.source))
        for key, value in nested_objects.items():
            validated_data[key] = value
        instance = nested_serializer.Meta.model.objects.create(**validated_data)
        return instance

    def create(self, validated_data):
        return self.deep_create(validated_data, self)


class TwitchUserSerializer(ModelSupportNestedSerializer):
    class Meta:
        model = TwitchUser
        fields = ('id', 'twid', 'name')


class ChannelSerializer(ModelSupportNestedSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'twid')


class StreamerSerializer(ModelSupportNestedSerializer):
    twitch_user = TwitchUserSerializer(many=False, read_only=False)
    channel = ChannelSerializer(many=False, read_only=False)

    class Meta:
        model = Streamer
        fields = ('id', 'twitch_user', 'channel')


class GameSerializer(ModelSupportNestedSerializer):
    class Meta:
        model = Game
        fields = ('id', 'twid', 'name')


class VideoSerializer(ModelSupportNestedSerializer):
    streamer = StreamerSerializer(many=False, read_only=False)
    game = GameSerializer(many=False, read_only=False)

    class Meta:
        model = Video
        fields = ('id', 'twid', 'streamer', 'game', 'recorded', 'length')


class ClipSerializer(ModelSupportNestedSerializer):
    streamer = StreamerSerializer(many=False, read_only=False)
    video = VideoSerializer(many=False, read_only=False)
    creator = TwitchUserSerializer(many=False, read_only=False)

    class Meta:
        model = Clip
        fields = ('id', 'streamer', 'video', 'creator', 'offset',
                  'duration', 'created', 'added', 'slug', 'title', 'views')


class EmoticonSerializer(ModelSupportNestedSerializer):
    streamer = StreamerSerializer(many=False, read_only=False)

    class Meta:
        model = Emoticon
        fields = ('id', 'twid', 'set_id', 'streamer', 'text')


class ChatSerializer(ModelSupportNestedSerializer):
    video = VideoSerializer(many=False, read_only=False)

    class Meta:
        model = Chat
        fields = ('id', 'video')


class MessageSerializer(ModelSupportNestedSerializer):
    chat = ChatSerializer(many=False, read_only=False)
    twitch_user = TwitchUserSerializer(many=False, read_only=False)

    class Meta:
        model = Message
        fields = ('id', 'chat', 'twitch_user', 'text', 'time')
