from ..models import PlayingTimeFrame, Court


def get_actual_timeframes():
    timeframes = PlayingTimeFrame.objects.all()
    return timeframes