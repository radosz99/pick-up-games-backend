from datetime import datetime, timedelta
import logging
from enum import Enum
import pytz

from ..exceptions import InvalidRequestException
from ..models import Court
from ..constants import R


utc = pytz.UTC


def rate_court(court_id, request):
    logging.debug(f"Trying to rate court with id {court_id}")
    rating = parse_rating_from_request(request)
    return {"stars": rating}


def get_timeframes_frequency(court_id, request):
    court = Court.objects.get(id=court_id)
    logging.debug(f"Looking for timeframes frequency for court with id {court_id} and name {court.name}")
    start_date, end_date = parse_dates_from_request(request)
    logging.debug(f"Dates given by user - start: {start_date}, end: {end_date}")
    intervals = get_30_minutes_intervals_dict_between_two_dates(start_date, end_date)
    court_timeframes = court.timeframes.all()
    logging.debug(f"Court has a total of {len(court_timeframes)} timeframes")
    for timeframe in court_timeframes:
        logging.debug(f"Checking timeframe - {timeframe}")
        for interval in intervals:
            logging.debug(f"Checking interval - {interval} + 30 minutes if it fits in timeframe")
            interval = convert_date_string_to_date(interval)
            if check_if_interval_is_between_two_dates(interval, timeframe.start, timeframe.end):
                logging.debug("Interval fits, so the value will be incremented")
                intervals[convert_date_to_date_string(interval)] += 1
    return intervals


def get_courts_list(request, serializer):
    queryset = Court.objects.all()
    logging.debug("Getting courts list")
    try:
        # if request contains user coordinates then courts are sorted by distance from given coordinates
        latitude = float(request.query_params.get('lat'))
        longitude = float(request.query_params.get('lon'))
        logging.debug(f"Getting courts sorted by distance from - lat = {latitude}, lon = {longitude}")
        serializer_data = serializer(queryset, many=True, context={'lat': latitude, 'lon': longitude}).data
        return sorted(serializer_data, key=lambda k: k['distance'], reverse=False)
    except TypeError:
        logging.debug("Parameters latitude or longitude not included in query params, returning normal list")
        serializer_data = serializer(queryset, many=True).data
        return serializer_data


def parse_rating_from_request(request):
    rating = request.query_params.get('rating')
    if rating is None:
        raise InvalidRequestException("Request should contain 'rating' query param")
    try:
        return float(rating)
    except ValueError:
        raise InvalidRequestException("`rating` param should be float")


def parse_dates_from_request(request):
    start, end = request.query_params.get('start'), request.query_params.get('end')
    if start is None or end is None:
        raise InvalidRequestException("Request should contain both 'start' and 'end' query params")
    start_date = convert_unix_timestamp_to_date(start)
    end_date = convert_unix_timestamp_to_date(end)
    return round_date(start_date, RoundType.DOWN), round_date(end_date, RoundType.UP)


def check_if_interval_is_between_two_dates(interval, start_date, end_date):
    interval = utc.localize(interval)
    logging.debug(f"Checking if interval - {interval} - {interval + timedelta(minutes=30)} is between {start_date} and {end_date}")
    if interval >= start_date and interval + timedelta(minutes=30) <= end_date:
        return True
    else:
        return False


def get_30_minutes_intervals_dict_between_two_dates(start_date, end_date):
    logging.debug(f"Looking for intervals between {start_date} and {end_date}")
    intervals = {}
    while end_date > start_date:
        intervals[convert_date_to_date_string(start_date)] = 0
        start_date = start_date + timedelta(minutes=30)
    logging.debug(f"Created list of intervals - {intervals}")
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
        logging.warning(f"Cannot convert {unix_timestamp} to date, invalid format")
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
    lat_1, lon_1 = radians(lat_1), radians(lon_1)
    lat_2, lon_2 = radians(lat_2), radians(lon_2)
    return haversine_formula(lat_1, lon_1, lat_2, lon_2)
