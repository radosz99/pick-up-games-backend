from enum import Enum
from datetime import datetime, timezone
import logging

from rest_framework.response import Response
from rest_framework import status

from ..models import Court
from ..exceptions import InvalidRequestException, TooManyRequestsFromIpException


def validate_ip(model, validation_type, value):
    """ Check if user with given IP has not rated court before """
    def inner(func):
        def wrapper(*args, **kwargs):
            request = args[1]
            ip = get_client_ip_from_request(request)
            try:
                validator = IPValidator(model, ip, request.data['court'])
                validator.validate(validation_type, value)
                kwargs['ip'] = ip
                response = func(*args, **kwargs)
                return response
            except (InvalidRequestException, TooManyRequestsFromIpException) as e:
                logging.info(str(e))
                return Response({"detail": str(e), "exception": e.__class__.__name__}, status=status.HTTP_403_FORBIDDEN)
        return wrapper
    return inner


def get_client_ip_from_request(request):
    logging.debug(f"Request META - {request.META}")
    ip = request.META.get('HTTP_X_REAL_IP')
    if ip is None:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    return ip


def parse_parameter_from_query_parameters(request, key, data_type=None):
    logging.debug(f"Parsing parameter '{key}' from request query parameters = {request.query_params} to type {data_type}")
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


class ValidationType(Enum):
    AMOUNT = 1
    TIME_ELAPSED = 2


class IPValidator:
    def __init__(self, model, user_ip, court_id):
        logging.info(f"Getting objects of {model} filtering by 'ip' = {user_ip} and 'court_id' = {court_id}")
        self.validate_if_court_exists(court_id)
        self.user_ip = user_ip
        self.model = model.__name__
        self.court_id = court_id
        self.objects = model.objects.filter(user_ip=user_ip).filter(court=court_id).order_by('-creation_date')
        logging.debug(f"Objects of {model} - {self.objects}")

    def validate(self, validation_type, validation_value):
        logging.info(f"Validating ip based on {validation_type} with validation value =  {str(validation_value)}")
        if not self.objects:
            logging.info(f"IP validation successful, no objects created from given IP for given court")
        elif validation_type is ValidationType.AMOUNT:
            if len(self.objects) >= validation_value:
                raise TooManyRequestsFromIpException(f"IP validation not successful, total number "
                                                     f"({len(self.objects)}) of {self.model} objects created in "
                                                     f"database from ip = {self.user_ip} for court_id = "
                                                     f"{self.court_id} has exceeded or is equal to maximum "
                                                     f"allowed ({validation_value})")
            else:
                logging.info(f"IP validation successful, {validation_value} > {len(self.objects)}")
        elif validation_type is ValidationType.TIME_ELAPSED:
            now = datetime.now(timezone.utc)
            difference = now - self.objects[0].creation_date
            if validation_value >= difference:
                raise TooManyRequestsFromIpException(f"IP validation not successful, last created {self.model} "
                                                     f"object from ip {self.user_ip} for court_id = {self.court_id} "
                                                     f"had been created on {self.objects[0].creation_date}, only "
                                                     f"{difference} time has elapsed till now ({now}) and minimum is "
                                                     f"= {validation_value}")
            else:
                logging.info(f"IP validation successful, {validation_value} >= {now - self.objects[0].creation_date}")

    def validate_if_court_exists(self, court_id):
        if not Court.objects.filter(id=court_id).exists():
            raise InvalidRequestException(f"Court with id = {court_id} does not exist")

