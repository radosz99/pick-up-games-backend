from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Court
from .serializers import CourtSerializer


class CourtViews(APIView):
    def get(self, request, id=None):
        if id:
            court = Court.objects.get(id=id)
            serializer = CourtSerializer(court)
        else:
            courts = Court.objects.all()
            serializer = CourtSerializer(courts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourtSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

