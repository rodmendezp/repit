import collections
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.utils import model_meta
from twitchdata.models import *


# TODO: Support Update for nested models
# TODO: Find another way to obtain _writable_fields from serializer
# WHY? the first but not so important problem is that is a protected field and should not be accessed
# The second and more important, this variable does not exist if data has not been serialized, and
# I am accessing _declared_fields (in test) which is not necessarily the same but solves the problem for now
# (but it is still a protected field, so cause confusion and do not solve the problem)
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

    def deep_ordered_to_returndict(self, data, serializer):
        writable_fields = serializer._writable_fields
        get_field_serializer = lambda x, y: list(filter(lambda _x: _x.source == y, x))[0]
        for key, value in data.items():
            if isinstance(value, collections.OrderedDict):
                nested_serializer = get_field_serializer(writable_fields, key)
                data[key] = self.deep_ordered_to_returndict(value, nested_serializer)
        return ReturnDict(data, serializer=serializer)

    # property data modified to return dict for nested models instead of ordered dict
    @property
    def data(self):
        ret = super(serializers.Serializer, self).data
        return self.deep_ordered_to_returndict(ret, self)

    # This function will create the corresponding model if there are no serializer fields,
    # if there are, it will create the nested model and then continue
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

    # Override create to support writable nested models
    def create(self, validated_data):
        return self.deep_create(validated_data, self)

    @staticmethod
    def get_model_nested_serializer(serializer, field_name):
        for field in serializer._writable_fields:
            if field.source == field_name:
                return field.Meta.model
        return None

    # Supports nested models. If id is not give it will assumes it has to create
    # a new instance of the nested object.
    # TODO: Need to make it recursive later and make different cases clearer
    def deep_update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            # If attr is a related model
            if attr in info.relations:
                field = getattr(instance, attr)
                # If id is the same do not do nothing
                if 'id' in value and field.id == value['id']:
                    pass
                # if id is different get the object by id and change it
                elif 'id' in value and field.id != value['id']:
                    try:
                        new_value = field._meta.model.objects.get(pk=value['id'])
                        setattr(instance, attr, new_value)
                    except models.ObjectDoesNotExist:
                        pass
                # if no id it creates a object for the nested model
                else:
                    model = self.get_model_nested_serializer(self, attr)
                    new_value = model.objects.create(**validated_data[attr])
                    setattr(instance, attr, new_value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    # Override update to support writable nested models
    def update(self, instance, validated_data):
        return self.deep_update(instance, validated_data)


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
    recorded = serializers.DateTimeField()
    length = serializers.TimeField()

    class Meta:
        model = Video
        fields = ('id', 'twid', 'streamer', 'game', 'recorded', 'length')


class ClipSerializer(ModelSupportNestedSerializer):
    streamer = StreamerSerializer(many=False, read_only=False)
    video = VideoSerializer(many=False, read_only=False)
    creator = TwitchUserSerializer(many=False, read_only=False)
    offset = serializers.TimeField()
    duration = serializers.TimeField()
    created = serializers.DateTimeField()
    added = serializers.DateTimeField()

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
    time = serializers.TimeField()

    class Meta:
        model = Message
        fields = ('id', 'chat', 'twitch_user', 'text', 'time')
