import json
from datetime import datetime, time
from twitchdata.models import *


class GameDoesNotExist(Exception):
    pass


def add_pk_fields(entries):
    for entry in entries:
        entry['fields']['pk'] = entry['pk']
    return entries


def get_streamers(game=None):
    with open('filler_debug.json', 'r') as f:
        filler_data = json.load(f)
        f.close()
    streamers = add_pk_fields(filler_data['filler_streamers'])
    streamers = list(map(lambda x: x['fields'], streamers))
    if game:
        games = add_pk_fields(filler_data['filler_games'])
        games = list(map(lambda x: x['fields'], games))
        if game not in list(map(lambda x: x['name'], games)):
            raise GameDoesNotExist
        game_entry = list(filter(lambda x: x['name'] == game, games))[0]
        streamers_games = filler_data['filler_streamers_games']
        streamers_games = list(filter(lambda x: x['fields']['game'] == game_entry['pk'], streamers_games))
        streamer_result = []
        for streamer_game in streamers_games:
            streamer_result.append(list(filter(lambda x: x['pk'] == streamer_game['fields']['streamer'], streamers))[0])
        streamer_result = list(map(lambda x: x['name'], streamer_result))
        streamers = {'streamers': streamer_result}
    print('Resulting streamers = ', streamers)
    return streamers


def get_games():
    with open('filler_debug.json', 'r') as f:
        filler_data = json.load(f)
        f.close()
    games = list(map(lambda x: x['fields'], filler_data['filler_games']))
    return games


def get_task():
    video_twid = 332415895
    try:
        Video.objects.get(twid=video_twid)
    except Video.DoesNotExist:
        print('IN VIDEO NOT EXIST EXCEPTION')
        try:
            streamer = Streamer.objects.get(twitch_user__name='chocotaco')
        except Streamer.DoesNotExist:
            twitch_user = TwitchUser.objects.create(name='chocotaco', twid=1)
            channel = Channel.objects.create(twid=1)
            streamer = Streamer(twitch_user=twitch_user, channel=channel)
        try:
            game = Game.objects.get(name="PLAYERUNKNOWN'S BATTLEGROUNDS")
        except Game.DoesNotExist:
            game = Game.objects.create(name="PLAYERUNKNOWN'S BATTLEGROUNDS", twid=1)
        Video.objects.create(twid=video_twid, streamer=streamer, game=game,
                             recorded=datetime.now(), length=time(hour=5, minute=2, second=7))

    return {
        'task': {
            'video_id': 332415895,
            'st_time': 1462,
            'end_time': 1470,
        }
    }
