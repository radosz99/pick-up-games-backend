from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .api.courts import CourtViewSet
from .api.timeframes import PlayingTimeFrameViewSet
from .api.court_details import SurfaceChoicesListView, RimTypeChoicesListView, CourtTypeChoicesListView

router = DefaultRouter()
router.register(r'court', CourtViewSet, basename='court')
router.register(r'timeframe', PlayingTimeFrameViewSet, basename='timeframe')

urlpatterns = [
    path('', include(router.urls)),
    path('court_details/surface', SurfaceChoicesListView.as_view()),
    path('court_details/type', CourtTypeChoicesListView.as_view()),
    path('court_details/rim', RimTypeChoicesListView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
