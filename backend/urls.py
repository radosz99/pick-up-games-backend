from django.urls import path

from .views import CourtViews

urlpatterns = [
    path('courts/<int:id>/', CourtViews.as_view()),
    path('courts', CourtViews.as_view())
]