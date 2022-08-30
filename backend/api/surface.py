from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import CourtDetails


class SurfaceChoicesListView(APIView):
    def get(self, request):
        choices = {counter: choice[1] for counter, choice in enumerate(CourtDetails.SurfaceType.choices)}
        return Response(choices)
