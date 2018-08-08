from .serializers import HighlightSerializer
from .models import Highlight
from rest_framework import generics


class HighlightList(generics.ListCreateAPIView):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer


class HighlightDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer
