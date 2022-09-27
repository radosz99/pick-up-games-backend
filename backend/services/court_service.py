from datetime import datetime, timedelta
from enum import Enum
import pytz

from ..exceptions import InvalidRequestException
from ..models import Court
from ..constants import R
from .request_utils import parse_parameter_from_query_parameters, DataType
from .. import logger

utc = pytz.UTC


def get_timeframes_frequency(court_id, request):
    court = Court.objects.get(id=court_id)
    logger.debug(f"Looking for timeframes frequency for court with id {court_id} and name {court.name}")
    start_date, end_date = parse_dates_from_request(request)
    logger.debug(f"Dates given by user - start: {start_date}, end: {end_date}")
    intervals = get_30_minutes_intervals_dict_between_two_dates(start_date, end_date)
    court_timeframes = court.timeframes.all()
    logger.debug(f"Court has a total of {len(court_timeframes)} timeframes")
    for timeframe in court_timeframes:
        logger.debug(f"Checking timeframe - {timeframe}")
        for interval in intervals:
            logger.debug(f"Checking interval - {interval} + 30 minutes if it fits in timeframe")
            interval = convert_date_string_to_date(interval)
            if check_if_interval_is_between_two_dates(interval, timeframe.start, timeframe.end):
                logger.debug("Interval fits, so the value will be incremented")
                intervals[convert_date_to_date_string(interval)] += 1
    return intervals


def sort_list(data, key, reverse=False):
    logger.debug(f"Sorting list by key = '{key}', reverse = '{reverse}'")
    return sorted(data, key=lambda k: k[key], reverse=reverse)


def get_court_with_distance(request, court, serializer):
    latitude = parse_parameter_from_query_parameters(request, 'lat', DataType.FLOAT)
    longitude = parse_parameter_from_query_parameters(request, 'lon', DataType.FLOAT)
    return serializer(court, context={'lat': latitude, 'lon': longitude}).data


def get_courts_list(request, serializer):
    queryset = Court.objects.all()
    logger.debug(f"Getting courts list, request query parameters = {request.query_params}")
    latitude = parse_parameter_from_query_parameters(request, 'lat', DataType.FLOAT)
    longitude = parse_parameter_from_query_parameters(request, 'lon', DataType.FLOAT)
    logger.debug(f"Getting courts with set distance from - lat = {latitude}, lon = {longitude}")
    serializer_data = serializer(queryset, many=True, context={'lat': latitude, 'lon': longitude}).data
    order_by = parse_parameter_from_query_parameters(request, 'order_by')
    reverse_order = parse_parameter_from_query_parameters(request, 'reverse', DataType.BOOL)
    logger.debug(f"Order query params: 'order_by' = {order_by}, 'reverse' = {reverse_order}")
    try:
        if order_by is not None:
            if reverse_order is not True:
                return sort_list(serializer_data, order_by)
            else:
                return sort_list(serializer_data, order_by, reverse=True)
        else:
            return serializer_data
    except (TypeError, KeyError) as e:
        logger.debug(f"Not possible to sort because = {str(e)}")
        raise InvalidRequestException(f"Wrong parameter for ordering, it is not possible to order by '{order_by}', "
                                      f"because of {e.__class__.__name__}: {str(e)}")


def parse_dates_from_request(request):
    start, end = request.query_params.get('start'), request.query_params.get('end')
    if start is None or end is None:
        raise InvalidRequestException("Request should contain both 'start' and 'end' query params")
    start_date = convert_unix_timestamp_to_date(start)
    end_date = convert_unix_timestamp_to_date(end)
    return round_date(start_date, RoundType.DOWN), round_date(end_date, RoundType.UP)


def check_if_interval_is_between_two_dates(interval, start_date, end_date):
    interval = utc.localize(interval)
    logger.debug(f"Checking if interval - {interval} - {interval + timedelta(minutes=30)} is between {start_date} and {end_date}")
    if interval >= start_date and interval + timedelta(minutes=30) <= end_date:
        return True
    else:
        return False


def get_30_minutes_intervals_dict_between_two_dates(start_date, end_date):
    logger.debug(f"Looking for intervals between {start_date} and {end_date}")
    intervals = {}
    while end_date > start_date:
        intervals[convert_date_to_date_string(start_date)] = 0
        start_date = start_date + timedelta(minutes=30)
    logger.debug(f"Created list of intervals - {intervals}")
    return intervals


def convert_date_string_to_date(str_date):
    return datetime.strptime(str_date, "%m/%d/%Y, %H:%M")


def convert_date_to_date_string(date):
    return date.strftime("%m/%d/%Y, %H:%M")


def convert_unix_timestamp_to_date(unix_timestamp):
    try:
        date = int(unix_timestamp)
        return datetime.fromtimestamp(date).replace(second=0, microsecond=0)
    except ValueError:
        logger.warning(f"Cannot convert {unix_timestamp} to date, invalid format")
        return datetime.fromtimestamp(0)


class RoundType(Enum):
    UP = 1
    DOWN = 2


def round_date(date, round_type):
    if round_type is RoundType.DOWN:
        if date.minute >= 30:
            date = date.replace(minute=30)
        else:
            date = date.replace(minute=0)
    elif round_type is RoundType.UP:
        if date.minute >= 30:
            date = date.replace(minute=0)
            date = date + timedelta(hours=1)
        else:
            date = date.replace(minute=0)
    return date


def haversine_formula(lat_1, lon_1, lat_2, lon_2):
    """ https://www.movable-type.co.uk/scripts/latlong.html """
    from math import sin, cos, sqrt, atan2
    difference_latitude = lat_1 - lat_2
    difference_longitude = lon_1 - lon_2
    a = sin(difference_latitude / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(difference_longitude / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def calculate_distance_between_two_coordinates(lat_1, lon_1, lat_2, lon_2):
    from math import radians
    logger.debug(f"Calculating distance between ({lat_1}, {lon_1}) and ({lat_2}, {lon_2})")
    lat_1, lon_1 = radians(lat_1), radians(lon_1)
    lat_2, lon_2 = radians(lat_2), radians(lon_2)
    return haversine_formula(lat_1, lon_1, lat_2, lon_2)


