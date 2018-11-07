import os
import re
from six.moves import xrange
from twitch.client import TwitchClient
from twitchchatdl.app.downloader import download
from twitchdata.models import TwitchUser, Video, Chat
from twitchdata.models import Message as TwitchDataMessage
from requests.exceptions import ConnectionError, HTTPError


class TwitchChat:
    def __init__(self, video_twid, file_path=None):
        self.twitch_client = TwitchClient('z7zaxcz22r4vzpdji9j2yxifzc63pl')
        self.messages = []
        self.user_names = set()
        self.twitch_users_db = {}
        self.video_twid = video_twid
        if not file_path:
            self.file_path = os.path.abspath(download(str(self.video_twid), 'z7zaxcz22r4vzpdji9j2yxifzc63pl'))
        else:
            self.file_path = file_path
        self.parse_file()

    def parse_file(self):
        with open(self.file_path, 'r', encoding='utf8') as f:
            for line in f:
                message = Message(line)
                if not message.is_valid():
                    continue
                self.messages.append(message)
                if message.user_name not in self.user_names:
                    self.user_names.add(message.user_name)

    def post_users(self):
        for user_name in self.user_names:
            twitch_user = TwitchUser.objects.filter(name=user_name)
            if len(twitch_user) == 1:
                self.twitch_users_db[user_name] = twitch_user[0]
        names_to_add = list(filter(lambda x: x not in self.twitch_users_db.keys(), self.user_names))
        for user_names_group in chunks(names_to_add, 99):
            try:
                twitch_users = self.twitch_client.users.translate_usernames_to_ids(user_names_group)
                for twitch_user in twitch_users:
                    data = {
                        'twid': twitch_user['id'],
                        'name': twitch_user['name']
                    }
                    try:
                        new_twitch_user = TwitchUser.objects.get(twid=twitch_user['id'])
                    except TwitchUser.DoesNotExist:
                        new_twitch_user = TwitchUser.objects.create(**data)
                    self.twitch_users_db[twitch_user['name']] = new_twitch_user
            except ConnectionError:
                print('There was a ConnectionError')
            except HTTPError:
                print('There was a HTTPError')

    def post_chat(self):
        video = Video.objects.get(twid=self.video_twid)
        return Chat.objects.create(video=video)

    def post_messages(self, chat):
        for message in self.messages:
            twitch_user = self.twitch_users_db.get(message.user_name, None)
            if twitch_user:
                TwitchDataMessage.objects.create(chat=chat, twitch_user=twitch_user, text=message.text, time=message.timestamp)
        return

    def add_to_twitch_data(self):
        self.post_users()
        chat = self.post_chat()
        self.post_messages(chat)


class Message:
    regex = '\[(\d{1,2}:\d{2}:\d{2})\]\s?\<([^\>]*)\>\s?(.+)'

    def __init__(self, message_text):
        r = re.search(self.regex, message_text)
        if not r:
            print('Invalid message: ', message_text)
            return
        self.timestamp = r.group(1)
        self.user_name = r.group(2)
        self.text = r.group(3)
        self.fix()

    def fix(self):
        self.user_name = self.user_name.replace(' ', '_')

    def is_valid(self):
        # User name will be invalid if it has oriental characters (DB does not support them)
        for c in self.user_name:
            ord_c = ord(c)
            if 0x4e00 <= ord_c <= 0x9fff or 0x30A0 <= ord_c <= 0x30ff or 0xac00 <= ord_c <= 0xd7af:
                return False
        return True


def chunks(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))
