from .serializers import HighlightSerializer, TypeSerializer
from .models import Highlight, Type
from twitchdata.models import Video
from django.http import Http404
from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from datetime import time


def seconds_to_hms(seconds):
    h = int(seconds / 3600)
    seconds -= h * 3600
    m = int(seconds / 60)
    seconds -= m * 60
    return {
        'hour': h,
        'minute': m,
        'second': seconds
    }


class TypeList(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class HighlightList(generics.ListCreateAPIView):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer

    # TODO: VideoID should be changed for VideoTWID to not confuse
    def post(self, request, *args, **kwargs):
        required_fields = ['video', 'start', 'end']
        for field in required_fields:
            if not request.data.get(field):
                return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
        try:
            video = Video.objects.get(twid=request.data['video'])
        except Video.DoesNotExist as e:
            return Response(data=repr(e), status=status.HTTP_400_BAD_REQUEST)
        try:
            type = Type.objects.get(name=request.data['type'])
        except Type.DoesNotExist as e:
            return Response(data=repr(e), status=status.HTTP_400_BAD_REQUEST)
        data = {
            'video': video,
            'user': request.user,
            'type': type,
            'start': time(**seconds_to_hms(request.data['start'])),
            'end': time(**seconds_to_hms(request.data['end'])),
            'labeled': True,
        }
        try:
            Highlight.objects.create(**data)
        except Exception as e:
            return Response(data=repr(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class HighlightDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer

    @staticmethod
    def get_by_pk(pk):
        try:
            return Highlight.objects.get(pk=pk)
        except Highlight.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        required_fields = ['type_id', 'description', 'start', 'end']
        for field in required_fields:
            if not request.data.get(field):
                return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
        try:
            highlight = self.get_by_pk(kwargs['pk'])
            highlight.user = request.user
            highlight.type_id = request.data['type_id']
            highlight.description = request.data['description']
            highlight.start = request.data['start']
            highlight.end = request.data['end']
            highlight.created = datetime.now()
            highlight.labeled = True
            highlight.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=repr(e), status=status.HTTP_400_BAD_REQUEST)
