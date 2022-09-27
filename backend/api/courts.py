import logging
import json

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from ..models import Court
from ..serializers import CourtSerializer
from ..services import court_service, image_service
from ..pagination import StandardResultsSetPagination
from ..exceptions import InvalidRequestException


class CourtViewSet(ModelViewSet):
    serializer_class = CourtSerializer
    queryset = Court.objects.all()
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'delete']

    def list(self, request, *args, **kwargs):
        serializer_data = court_service.get_courts_list(request, self.serializer_class)
        page = self.paginate_queryset(serializer_data)
        return self.get_paginated_response(page)

    @action(detail=True, url_path='timeframes', methods=['get'])
    def get_timeframes(self, request, pk=None):
        try:
            data = court_service.get_timeframes_frequency(pk, self.request)
            return Response(data)
        except InvalidRequestException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, url_path='images', methods=['get'])
    def get_images(self, request, pk=None):
        data = image_service.get_court_images(pk)
        return Response(data)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)
