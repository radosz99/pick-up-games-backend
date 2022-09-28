from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from ..models import Rating
from ..serializers import RatingSerializer
from ..services.request_utils import validate_ip, ValidationType


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    http_method_names = ['get', 'post']

    @validate_ip(model=Rating, validation_type=ValidationType.AMOUNT, value=1)
    def create(self, request, *args, **kwargs):
        request.data['user_ip'] = kwargs['ip']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
