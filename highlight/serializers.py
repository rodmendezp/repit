from rest_framework import serializers
from .models import Highlight
from twitchdata.serializers import VideoSerializer


class HighlightSerializer(serializers.ModelSerializer):
    video = VideoSerializer()

    class Meta:
        model = Highlight
        fields = ('video', 'start', 'end')
