import json
import requests
from channels.generic.websocket import AsyncWebsocketConsumer


class FillerAPI:
    def __init__(self):
        self.baseURL = 'http://127.0.0.1:9999/filler/'

    def jobs_available(self, game, streamer='', user=''):
        params = {
            'game': game,
            'streamer': streamer,
            'user': user,
        }
        response = requests.get(self.baseURL + 'jobs_available', params)
        data = json.loads(response.text)
        if data['jobs_available'] == 'yes':
            return data['job']
        return False

    def filler_status(self, game, streamer='', user=''):
        params = {
            'game': game,
            'streamer': streamer,
            'user': user,
        }
        response = requests.get(self.baseURL + 'status', params)
        data = json.loads(response.text)
        return data['status_short']

    def request_jobs(self, game, streamer='', user=''):
        params = {
            'game': game,
            'streamer': streamer,
            'user': user,
        }
        response = requests.get(self.baseURL + 'request_jobs', params)
        data = json.loads(response.text)
        return data['request_response']

    def cancel_jobs(self, game, streamer='', user=''):
        params = {
            'game': game,
            'streamer': streamer,
            'user': user,
        }
        response = requests.get(self.baseURL + 'cancel_jobs', params)
        data = json.loads(response.text)
        return data['cancel_response']


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.fillerAPI = FillerAPI()
        super().__init__(*args, **kwargs)

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        params = text_data_json['params']
        print('Recieved Message = ', message)
        print('Params = ', params)
        game = self.replace_game_characters(params.get('game', ''))
        streamer = params.get('streamer', '')
        user = params.get('user', '')

        if message == 'GET_HIGHLIGHT':
            job_available = self.fillerAPI.jobs_available(game, streamer, user)
            if not job_available:
                filler_status = self.fillerAPI.filler_status(game, streamer, user)
                if filler_status != 'processing':
                    self.fillerAPI.request_jobs(game, streamer, user)
                await self.send(text_data=json.dumps({
                    'message': 'LOADING'
                }))
            else:
                await self.send(text_data=json.dumps({
                    'message': {
                        'video_id': int(job_available['video_id']),
                        'st_time':  int(job_available['st_time']),
                        'end_time': int(job_available['end_time']),
                        'delivery_tag': int(job_available['delivery_tag'])
                    }
                }))
        else:
            await self.send(text_data=json.dumps({
                'message': 'ERROR'
            }))

    @staticmethod
    def replace_game_characters(game):
        game = game.replace(' ', '_')
        game = game.replace('-', '_')
        game = game.replace("'", '_')
        game = game.replace(':', '_')
        game = game.replace('__', '_')
        return game.replace('.', '_').lower()





