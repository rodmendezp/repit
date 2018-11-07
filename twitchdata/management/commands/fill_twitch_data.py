import os
from datetime import time
from twitch.client import TwitchClient
from twitchdata.models import *
from highlight.models import *
from twitchdata.utils.twich_chat import TwitchChat
from django.core.management.base import BaseCommand
from requests.exceptions import ConnectionError, HTTPError


class Command(BaseCommand):
    help = ''

    def __init__(self, stdout=None, stderr=None, no_color=False):
        self.twitch_client = None
        super().__init__(stdout, stderr, no_color)

    def add_arguments(self, parser):
        parser.add_argument('chat_folder')

    def handle(self, *args, **options):
        self.twitch_client = TwitchClient('z7zaxcz22r4vzpdji9j2yxifzc63pl')
        chat_folder = options['chat_folder']
        highlights = Highlight.objects.all()
        for highlight in highlights:
            video_file_name = 'v%s.txt' % highlight.video.twid
            streamer = highlight.video.streamer.twitch_user.name
            chat_file_path = os.path.join(chat_folder, streamer, video_file_name)
            if not os.path.exists(chat_file_path):
                twitch_chat = TwitchChat(highlight.video.twid)
                streamer_folder = os.path.join(chat_folder, streamer)
                if not os.path.exists(streamer_folder):
                    os.mkdir(streamer_folder)
                os.rename(twitch_chat.file_path, os.path.join(streamer_folder, video_file_name))
        messages_added = 0
        files_added = 0
        streamer_folders = os.listdir(chat_folder)
        for streamer_folder in streamer_folders:
            chats = os.listdir(os.path.join(chat_folder, streamer_folder))
            for chat in chats:
                video_twid = chat.replace('v', '').replace('.txt', '')
                twitch_data_chat = Chat.objects.filter(video__twid=video_twid)
                if twitch_data_chat and len(twitch_data_chat) > 0:
                    continue
                try:
                    Video.objects.get(twid=video_twid)
                except Video.DoesNotExist:
                    try:
                        self.add_video(video_twid)
                    except HTTPError:
                        continue
                twitch_chat = TwitchChat(video_twid, os.path.join(chat_folder, streamer_folder, chat))
                twitch_chat.add_to_twitch_data()

    def add_video(self, video_twid):
        video = self.twitch_client.videos.get_by_id(video_twid)
        streamer = Streamer.objects.filter(twitch_user__name=video['channel']['name'])
        streamer = streamer[0] if streamer and len(streamer) > 0 else None
        if not streamer:
            twitch_user = TwitchUser.objects.filter(name=video['channel']['name'])
            twitch_user = twitch_user[0] if twitch_user and len(twitch_user) > 0 else None
            if not twitch_user:
                twitch_user = TwitchUser.objects.create(twid=video['channel']['id'], name=video['channel']['name'])
            channel = Channel.objects.filter(twid=video['channel']['id'])
            channel = channel[0] if channel and len(channel) > 0 else None
            if not channel:
                channel = Channel.objects.create(twid=video['channel']['id'])
            streamer = Streamer.objects.create(twitch_user=twitch_user, channel=channel)
        game = Game.objects.filter(name=video['game'])
        game = game[0] if game and len(game) > 0 else None
        if not game:
            game_twid = self.get_game_twid(video['game'])
            game = Game.objects.create(name=video['game'], twid=game_twid)
        video_instance = Video()
        video_instance.twid = video_twid
        video_instance.streamer = streamer
        video_instance.game = game
        video_instance.recorded = video['created_at']
        video_instance.length = time(**self.seconds_to_h_m_s(video['length']))
        video_instance.save()

    def get_game_twid(self, game):
        games = self.twitch_client.games.get_top()
        games = list(filter(lambda x: x['game']['name'] == game, games))
        return games[0]['game']['id']

    @staticmethod
    def seconds_to_h_m_s(secs):
        h = int(secs / 3600)
        secs -= h * 3600
        m = int(secs / 60)
        secs -= m * 60
        return {
            'hour': h,
            'minute': m,
            'second': secs
        }


