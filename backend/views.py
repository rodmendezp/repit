import json
from rest_framework.views import APIView
from fillerapi.client import FillerClient


class TaskView(APIView):
    def get(self, request):
        filler_client = FillerClient()
        response = filler_client.task.get(request.query_params)
        data = json.loads(response.content)
        if data['task'] is not None:
            return response
        response = filler_client.status.get(request.query_params)
        data = json.loads(response.content)
        if not data['queue_status']['processing']:
            response = filler_client.process.get(request.query_params)
        return response

    def post(self, request):
        filler_client = FillerClient()
        response = filler_client.task.post(request.data)
        return response


class FillerGame(APIView):
    def get(self, request):
        filler_client = FillerClient()
        response = filler_client.filler_game.get_objects_response(request.query_params)
        return response


class FillerStreamer(APIView):
    def get(self, request):
        filler_client = FillerClient()
        game = request.query_params.get('game', None)
        game_defaults = request.query_params.get('game_defaults', None)
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
