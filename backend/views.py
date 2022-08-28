from rest_framework import generics

from .models import Court
from .serializers import CourtSerializer


class ListCourt(generics.ListAPIView):
    queryset = Court.objects.all()
    print(queryset)
    serializer_class = CourtSerializer


class DetailCourt(generics.RetrieveAPIView):
    queryset = Court.objects.all()
    serializer_class = CourtSerializer
