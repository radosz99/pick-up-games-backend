from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import CourtDetails


class CourtDetailsChoicesListView(APIView):
    @staticmethod
    def get_list_of_choices(model):
        return [choice[1] for choice in model.choices]

    def get(self, request):
        surface_choices = self.get_list_of_choices(CourtDetails.SurfaceType)
        rim_choices = self.get_list_of_choices(CourtDetails.RimType)
        court_choices = self.get_list_of_choices(CourtDetails.CourtType)
        choices = {
            "rim_type": rim_choices,
            "court_type": court_choices,
            "surface_type": surface_choices
        }
        return Response(choices)

