from django.urls import path
from .api.courts import CourtViews


urlpatterns = [
    path('courts/<int:id>/', CourtViews.as_view()),
    path('courts', CourtViews.as_view()),
]