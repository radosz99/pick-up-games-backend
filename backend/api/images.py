from ..models import CourtImage
from ..serializers import ImageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser


class MyModelViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]

    http_method_names = ['get']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)