from django.urls import path

from .views import ListCourt, DetailCourt

urlpatterns = [
    path('<int:pk>/', DetailCourt.as_view()),
    path('', ListCourt.as_view())
]