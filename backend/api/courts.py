from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from ..models import Court
from ..serializers import CourtSerializer
from ..services import court_service, image_service


class CourtViewSet(ModelViewSet):
    serializer_class = CourtSerializer
    queryset = Court.objects.all()
    http_method_names = ['get', 'post', 'delete']

    @action(detail=True, url_path='timeframes', methods=['get'])
    def get_timeframes(self, request, pk=None):
        data = court_service.get_timeframes_frequency(pk, self.request)
        return Response(data)

    @action(detail=True, url_path='images', methods=['get'])
    def get_images(self, request, pk=None):
        data = image_service.get_court_images(pk)
        return Response(data)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)
