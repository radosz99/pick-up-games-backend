from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import Court
from ..serializers import CourtSerializer
from ..services import court_service


class CourtViewSet(ModelViewSet):
    serializer_class = CourtSerializer
    queryset = Court.objects.all()
    http_method_names = ['get', 'post']

    @action(detail=True, url_path='timeframes', methods=['get'])
    def get_timeframes(self, request, pk=None):
        data = court_service.get_timeframes_frequency(pk, self.request)
        return Response(data)
