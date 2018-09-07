from rest_framework import serializers
from .models import Highlight, Type
from twitchdata.serializers import VideoSerializer
from backend.serializers import UserSerializer


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'name', 'parent')


class HighlightSerializer(serializers.ModelSerializer):
    video = VideoSerializer()
    user = UserSerializer()
    type = TypeSerializer()
    start = serializers.TimeField()
    end = serializers.TimeField()
    created = serializers.DateTimeField()

    class Meta:
        model = Highlight
        fields = ('video', 'user', 'type', 'description',
                  'start', 'end', 'created', 'labeled', 'validated')
