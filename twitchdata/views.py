import json

from twitchdata.serializers import *
from twitchdata.models import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class TwitchDataLOPagination(LimitOffsetPagination):
    default_limit = 100
    max_default = 1000


class TwitchUserList(generics.ListCreateAPIView):
    queryset = TwitchUser.objects.all()
    serializer_class = TwitchUserSerializer

    # TODO: See if it is viable to have a generic 'get_queryset' function
    def get_queryset(self):
        queryset = TwitchUser.objects.all()
        twid = self.request.query_params.get('twid', None)
        name = self.request.query_params.get('name', None)
        queryset = queryset.filter(twid=twid) if twid else queryset
        queryset = queryset.filter(name=name) if name else queryset
        return queryset


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

    def get_queryset(self):
        queryset = Streamer.objects.all()
        streamer_name = self.request.query_params.get('streamer_name', None)
        queryset = queryset.filter(twitch_user__name=streamer_name) if streamer_name else queryset
        return queryset


class StreamerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Streamer.objects.all()
    serializer_class = StreamerSerializer


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        queryset = Game.objects.all()
        name = self.request.query_params.get('name', None)
        queryset = queryset.filter(name=name) if name else queryset
        return queryset


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class VideoList(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(self):
        queryset = Video.objects.all()
        twid = self.request.query_params.get('twid', None)
        queryset = queryset.filter(twid=twid) if twid else queryset
        return queryset

    @staticmethod
    def get_or_create_user(twid, name):
        twitch_user, _ = TwitchUser.objects.get_or_create(twid=twid, name=name)
        return twitch_user

    @staticmethod
    def get_or_create_channel(twid):
        channel, _ = Channel.objects.get_or_create(twid=twid)
        return channel

    @staticmethod
    def get_or_create_streamer(twid, name):
        try:
            return Streamer.objects.get(twitch_user__name=name, channel__twid=twid)
        except Streamer.DoesNotExist:
            return Streamer.objects.create(
                twitch_user=VideoList.get_or_create_user(twid, name),
                channel=VideoList.get_or_create_channel(twid)
            )

    @staticmethod
    def get_or_create_game(twid, name):
        game, _ = Game.objects.get_or_create(twid=twid, name=name)
        return game

    def post(self, request, *args, **kwargs):
        if request.data.get('twid', None) and request.data.get('streamer_twid', None):
            return self.post_twid(request)
        else:
            return super().post(request, *args, **kwargs)

    @staticmethod
    def post_twid(request):
        data = request.data
        twid = data['twid']
        streamer = VideoList.get_or_create_streamer(data['streamer_twid'], data['streamer_name'])
        game = VideoList.get_or_create_game(data['game_twid'], data['game_name'])
        recorded = json.loads(data['recorded'])
        length = json.loads(data['length'])
        Video.objects.create(twid=twid, streamer=streamer, game=game, recorded=recorded, length=length)
        return Response(status=status.HTTP_201_CREATED)


class VideoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class ClipList(generics.ListCreateAPIView):
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer

    def get_queryset(self):
        queryset = Clip.objects.all()
        streamer_name = self.request.query_params.get('streamer_name', None)
        video_twid = self.request.query_params.get('video_twid', None)
        slug = self.request.query_params.get('slug', None)
        queryset = queryset.filter(streamer__twitch_user__name=streamer_name) if streamer_name else queryset
        queryset = queryset.filter(video__twid=video_twid) if video_twid else queryset
        queryset = queryset.filter(slug=slug) if slug else queryset
        return queryset


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
