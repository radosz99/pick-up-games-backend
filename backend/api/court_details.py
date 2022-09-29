from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import CourtDetails


class CourtDetailsChoicesListView(APIView):
    def get(self, request):
        surface_choices = {counter: choice[1] for counter, choice in enumerate(CourtDetails.SurfaceType.choices)}
        rim_choices = {counter: choice[1] for counter, choice in enumerate(CourtDetails.RimType.choices)}
        court_choices = {counter: choice[1] for counter, choice in enumerate(CourtDetails.CourtType.choices)}
        choices = {
            "rim_type": rim_choices,
            "court_type": court_choices,
            "surface_type": surface_choices
        }
        return Response(choices)

