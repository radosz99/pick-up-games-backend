from ..models import Court
from ..exceptions import InvalidRequestException


def get_court_images(court_id):
    court = Court.objects.all().filter(id=court_id)
    if court:
        court = court[0]
    else:
        raise InvalidRequestException(f"Court with id = {court_id} does not exist")
    return court.images.all()
