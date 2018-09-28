import json
import requests
from channels.generic.websocket import AsyncWebsocketConsumer


class FillerAPI:
    def __init__(self):
        self.baseURL = 'http://127.0.0.1:9999/filler/'

    def jobs_available(self):
        response = requests.get(self.baseURL + 'jobs_available')
        data = json.loads(response.text)
        if data['jobs_available'] == 'yes':
            return data['job']
        return False

    def filler_status(self):
        response = requests.get(self.baseURL + 'status')
        data = json.loads(response.text)
        return data['status_short']

    def request_jobs(self):
        response = requests.get(self.baseURL + 'request_jobs')
        data = json.loads(response.text)
        return data['request_response']

    def cancel_jobs(self):
        response = requests.get(self.baseURL + 'cancel_jobs')
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
        print('Recieved Message = ', message)

        if message == 'GET_HIGHLIGHT':
            job_available = self.fillerAPI.jobs_available()
            if not job_available:
                filler_status = self.fillerAPI.filler_status()
                if filler_status != 'processing':
                    self.fillerAPI.request_jobs()
                await self.send(text_data=json.dumps({
                    'message': 'LOADING'
                }))
            else:
                await self.send(text_data=json.dumps({
                    'message': {
                        'video_id': job_available['video_id'],
                        'st_time':  job_available['st_time'],
                        'end_time': job_available['end_time'],
                    }
                }))
        else:
            await self.send(text_data=json.dumps({
                'message': 'ERROR'
            }))





