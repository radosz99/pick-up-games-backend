from rest_framework.viewsets import ModelViewSet

from ..models import Rating
from ..serializers import RatingSerializer


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    http_method_names = ['get', 'post']
