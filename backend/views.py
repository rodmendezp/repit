import json
from django.http import HttpResponse
from rest_framework.views import APIView
from fillerapi.client import FillerClient
from django.conf import settings
from backend import utils


class TaskView(APIView):
    @staticmethod
    def get(request):
        if settings.DEBUG_FILLER:
            return HttpResponse(json.dumps(utils.get_task()), content_type='application/json')
        filler_client = FillerClient()
        response = filler_client.task.get(request.query_params)
        data = json.loads(response.content)
        if 'task' in data and data['task'] is not None:
            return response
        elif 'exception' in data:
            return HttpResponse(json.dumps({'exception': data['exception']}), content_type='application/json')
        response = filler_client.status.get(request.query_params)
        data = json.loads(response.content)
        if not data['queue_status']['processing']:
            response = filler_client.process.get(request.query_params)
            return response
        else:
            data['message'] = 'Already processing'
            return HttpResponse(json.dumps(data), content_type='application/json')

    @staticmethod
    def post(request):
        if settings.DEBUG_FILLER:
            return HttpResponse(json.dumps({'status': 'SUCCEED'}), content_type='application/json')
        filler_client = FillerClient()
        response = filler_client.task.post(request.data)
        return response


class FillerGame(APIView):
    def get(self, request):
        if settings.DEBUG_FILLER:
            return HttpResponse(json.dumps(utils.get_games()), content_type='application/json')
        filler_client = FillerClient()
        response = filler_client.filler_game.get_objects_response(request.query_params)
        return response


class FillerStreamer(APIView):
    def get(self, request):
        game = request.query_params.get('game', None)
        game_defaults = request.query_params.get('game_defaults', None)
        if settings.DEBUG_FILLER:
            return HttpResponse(json.dumps(utils.get_streamers(game_defaults)), content_type='application/json')
        filler_client = FillerClient()
        if game:
            return filler_client.filler_streamer.get_game_current_streamers(game)
        elif game_defaults:
            return filler_client.filler_streamer.get_game_default_streamers(game_defaults)
        response = filler_client.filler_streamer.get_objects_response()
        return response


class GameQueueStatus(APIView):
    def get(self, request):
        filler_client = FillerClient()
        return filler_client.game_queue.get_objects(params=request.query_params)


class CustomQueueStatus(APIView):
    def get(self, request):
        filler_client = FillerClient()
        return filler_client.custom_queue.get_objects(params=request.query_params)
