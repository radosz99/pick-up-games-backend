from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.courts import CourtViewSet


router = DefaultRouter()
router.register(r'court', CourtViewSet, basename='court')

urlpatterns = [
    path('', include(router.urls))
]