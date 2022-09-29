from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.courts import CourtViewSet
from .api.timeframes import PlayingTimeFrameViewSet
from .api.ratings import RatingViewSet
from .api.comments import CommentViewSet
from .api.court_details import CourtDetailsChoicesListView

router = DefaultRouter()
router.register(r'court', CourtViewSet, basename='court')
router.register(r'timeframe', PlayingTimeFrameViewSet, basename='timeframe')
router.register(r'rating', RatingViewSet, basename='rating')
router.register(r'comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('court_details/choices', CourtDetailsChoicesListView.as_view()),
]
