from datetime import timedelta

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from ..models import Comment
from ..serializers import CommentSerializer
from ..services.request_utils import validate_ip, ValidationType, parse_parameter_from_query_parameters
from ..pagination import StandardResultsSetPagination


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post']

    @validate_ip(model=Comment, validation_type=ValidationType.TIME_ELAPSED, value=timedelta(minutes=60))
    def create(self, request, *args, **kwargs):
        request.data['user_ip'] = kwargs['ip']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        court_id = parse_parameter_from_query_parameters(request, 'court_id')
        if court_id is not None:
            queryset = self.queryset.filter(court_id=court_id)
        else:
            queryset = self.queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
