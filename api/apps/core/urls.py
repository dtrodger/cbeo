"""
Core app URL routing
"""
from django.urls import path

from apps.core.views import PitchUpload, PitchModelView, StatusView


urlpatterns = [
    path("pitch-upload/", PitchUpload.as_view(), name="pitch-upload"),
    path("pitch/", PitchModelView.as_view({"get": "list"}), name="pitch"),
    path("status/", StatusView.as_view(), name="status"),
]
