import json
from backend.models import *
from highlight.models import *
from twitchdata.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ''

    def __init__(self, stdout=None, stderr=None, no_color=False):
        self.models = {}
        self.db_models = {}
        self.default_user = None
        super().__init__(stdout, stderr, no_color)

    def add_arguments(self, parser):
        parser.add_argument('json_file_path')
        pass

    def handle(self, *args, **options):
        json_file_path = options['json_file_path']
        with open(json_file_path) as f:
            json_data = json.load(f)
        default_user = User.objects.filter(first_name='Default', last_name='User')
        default_user = default_user[0] if default_user and len(default_user) > 0 else None
        if not default_user:
            return
        self.default_user = default_user
        twitchuser_fields = ['twid', 'name']
        channel_fields = ['twid']
        streamer_fields = ['twitch_user', 'channel']
        game_fields = ['twid', 'name']
        video_fields = ['twid', 'streamer', 'game', 'recorded', 'length']
        type_fields = ['name', 'parent']
        highlight_fields = ['video', 'user', 'type', 'description', 'start', 'end', 'created', 'labeled', 'validated']
        self.models['twitch_user'] = {}
        self.models['channel'] = {}
        self.models['streamer'] = {}
        self.models['game'] = {}
        self.models['video'] = {}
        self.models['type'] = {}
        self.models['highlight'] = {}
        self.db_models['twitch_user'] = TwitchUser
        self.db_models['channel'] = Channel
        self.db_models['streamer'] = Streamer
        self.db_models['game'] = Game
        self.db_models['video'] = Video
        self.db_models['type'] = Type
        self.db_models['highlight'] = Highlight
        for entry in json_data:
            if entry['model'] == 'twitchdata.twitchuser':
                self.fill_model_dict(entry, self.models['twitch_user'], twitchuser_fields)
            elif entry['model'] == 'twitchdata.channel':
                self.fill_model_dict(entry, self.models['channel'], channel_fields)
            elif entry['model'] == 'twitchdata.streamer':
                self.fill_model_dict(entry, self.models['streamer'], streamer_fields)
            elif entry['model'] == 'twitchdata.game':
                self.fill_model_dict(entry, self.models['game'], game_fields)
            elif entry['model'] == 'twitchdata.video':
                self.fill_model_dict(entry, self.models['video'], video_fields)
            elif entry['model'] == 'highlight.type':
                self.fill_model_dict(entry, self.models['type'], type_fields)
            elif entry['model'] == 'highlight.highlight':
                self.fill_model_dict(entry, self.models['highlight'], highlight_fields)
        for pk, fields in self.models['highlight'].items():
            highlight = Highlight()
            for field, value in fields.items():
                if field == 'user':
                    setattr(highlight, field, self.default_user)
                elif field in self.models:
                    instance = self.get_instance(value, field) # do something
                    setattr(highlight, field, instance)
                else:
                    setattr(highlight, field, value)
            try:
                highlight.save()
            except Exception as e:
                print(e)
        return

    def get_instance(self, data, model_name):
        instance = None
        model = self.db_models[model_name]
        queryset = model.objects.all()
        for key, value in data.items():
            if len(queryset) == 0:
                break
            if key not in self.models:
                queryset = queryset.filter(**{key: value})
            else:
                sub_instance = self.get_instance(value, key)
                queryset = queryset.filter(**{key: sub_instance})
        if len(queryset) == 0:
            instance = model()
            for key, value in data.items():
                if key not in self.models:
                    setattr(instance, key, value)
                else:
                    sub_instance = self.get_instance(value, key)
                    setattr(instance, key, sub_instance)
            instance.save()
        elif len(queryset) == 1:
            instance = queryset[0]
        else:
            raise Exception
        return instance

    def fill_model_dict(self, entry, model_dict, fields):
        model_dict[entry['pk']] = {}
        for field in fields:
            if field == 'user':
                model_dict[entry['pk']][field] = self.default_user
            elif field not in self.models:
                model_dict[entry['pk']][field] = entry['fields'][field]
            else:
                model_dict[entry['pk']][field] = self.models[field][entry['fields'][field]]
