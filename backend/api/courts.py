from rest_framework.viewsets import ModelViewSet

from ..models import Court
from ..serializers import CourtSerializer


class CourtViewSet(ModelViewSet):
    serializer_class = CourtSerializer
    queryset = Court.objects.all()
