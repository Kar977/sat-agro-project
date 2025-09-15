from django.urls import path
from proxt_imgw.views import warnings_by_location, WarningListView, WarningDetailView

urlpatterns = [
    path("warnings/", WarningListView.as_view(), name="warnings-list"),
    path("warnings/<int:pk>/", WarningDetailView.as_view(), name="warnings-detail"),
    path("by_location/", warnings_by_location),
]
