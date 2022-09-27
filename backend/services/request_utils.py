import functools
import logging

from rest_framework.response import Response
from rest_framework import status

from ..models import Rating
from ..exceptions import TooManyRequestsFromIpException


def validate_ip(model):
    """ Check if user with given IP has not rated court before """
    def inner(func):
        def wrapper(*args, **kwargs):
            ip = get_client_ip(args[1])
            logging.debug(f"User IP is {ip}")
            if model.objects.filter(user_ip=ip).exists():
                logging.debug("User with this IP has already rated the court")
                return Response({"detail": f"User with this IP ({ip}) has already rated the court"}, status=status.HTTP_403_FORBIDDEN)
            else:
                value = func(*args, **kwargs)
                return value
        return wrapper
    return inner


def get_client_ip(request):
    logging.debug(f"Request META - {request.META}")
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
