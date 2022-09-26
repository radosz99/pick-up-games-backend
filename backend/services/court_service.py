from datetime import datetime, timedelta
import logging
from enum import Enum
import pytz

from ..exceptions import InvalidRequestException
from ..models import Court

utc = pytz.UTC


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


def parse_dates_from_request(request):
    start = request.query_params.get('start')
    end = request.query_params.get('end')
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


def calculate_distance(lat_1, lon_1, lat_2, lon_2):
    from math import sin, cos, sqrt, atan2, radians
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(lat_1)
    lon1 = radians(lon_1)
    lat2 = radians(lat_2)
    lon2 = radians(lon_2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance
