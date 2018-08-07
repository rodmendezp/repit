from twitchdata.serializers import *
from twitchdata.models import *
from rest_framework import generics


class TwitchUserList(generics.ListCreateAPIView):
    queryset = TwitchUser.objects.all()
    serializer_class = TwitchUserSerializer


class TwitchUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TwitchUser.objects.all()
    serializer_class = TwitchUserSerializer


class ChannelList(generics.ListCreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class ChannelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class StreamerList(generics.ListCreateAPIView):
    queryset = Streamer.objects.all()
    serializer_class = StreamerSerializer


class StreamerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Streamer.objects.all()
    serializer_class = StreamerSerializer


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class VideoList(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class ClipList(generics.ListCreateAPIView):
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer


class ClipDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer


class EmoticonList(generics.ListCreateAPIView):
    queryset = Emoticon.objects.all()
    serializer_class = EmoticonSerializer


class EmoticonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Emoticon.objects.all()
    serializer_class = EmoticonSerializer


class ChatList(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
