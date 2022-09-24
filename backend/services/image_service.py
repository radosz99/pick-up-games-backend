from ..models import CourtImage


def get_court_images(court_id):
    try:
        images = CourtImage.objects.get(id=court_id)
    except CourtImage.DoesNotExist:
        images = []
    return images