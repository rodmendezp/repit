from .serializers import HighlightSerializer, TypeSerializer
from .models import Highlight, Type
from django.http import Http404
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
        highlight = self.get_by_pk(kwargs['pk'])
        serializer = HighlightSerializer(highlight, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
