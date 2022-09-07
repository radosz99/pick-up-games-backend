from rest_framework.viewsets import ModelViewSet

from ..models import PlayingTimeFrame
from ..serializers import TimeFrameSerializer


class PlayingTimeFrameViewSet(ModelViewSet):
    serializer_class = TimeFrameSerializer
    queryset = PlayingTimeFrame.objects.all()
    http_method_names = ['get', 'post']
