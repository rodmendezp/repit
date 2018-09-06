from .serializers import HighlightSerializer, TypeSerializer
from .models import Highlight, Type
from django.http import Http404
from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response



class TypeList(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class HighlightList(generics.ListCreateAPIView):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer


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
            if not hasattr(request.data, field):
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
        except Exception as e:
            return Response(data=repr(e), status=status.HTTP_400_BAD_REQUEST)
