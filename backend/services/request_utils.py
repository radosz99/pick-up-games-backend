from enum import Enum

from rest_framework.response import Response
from rest_framework import status

from .. import logger


def validate_ip(model):
    """ Check if user with given IP has not rated court before """
    def inner(func):
        def wrapper(*args, **kwargs):
            request = args[1]
            ip = get_client_ip_from_request(request)
            court_id = request.data['court']
            logger.debug(f"Court id = {court_id}, user IP is {ip}")
            kwargs['ip'] = ip
            if model.objects.filter(user_ip=ip).filter(court=court_id).exists():
                logger.debug(f"User with this IP ({ip}) has already rated court with id {court_id}")
                return Response({"detail": f"User with this IP ({ip}) has already rated court with id {court_id}"}, status=status.HTTP_403_FORBIDDEN)
            else:
                value = func(*args, **kwargs)
                return value
        return wrapper
    return inner


def get_client_ip_from_request(request):
    logger.debug(f"Request META - {request.META}")
    ip = request.META.get('HTTP_X_REAL_IP')
    if ip is None:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    return ip


def parse_parameter_from_query_parameters(request, key, data_type=None):
    logger.debug(f"Parsing parameter '{key}' from request query parameters = {request.query_params} to type {data_type}")
    try:
        if data_type is DataType.BOOL:
            return request.query_params.get(key) == 'True'
        elif data_type is not None:
            return data_type.value(request.query_params.get(key))
        else:
            return request.query_params.get(key)
    except TypeError:
        return None


class DataType(Enum):
    INT = int
    FLOAT = float
    BOOL = bool
