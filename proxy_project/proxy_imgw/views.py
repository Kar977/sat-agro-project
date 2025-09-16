from django.utils import timezone
from geo_localization.utils import get_teryt_from_coords
from proxy_imgw.models import Warning
from proxy_imgw.serializers import WarningSerializer, LocationQuerySerializer
from proxy_imgw.services import get_warnings_for_location
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response


class WarningListView(generics.ListAPIView):
    """
    API view to list all meteorological warnings.
    """

    queryset = Warning.objects.all()
    serializer_class = WarningSerializer


class WarningDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single meteorological warning by its ID.
    """

    queryset = Warning.objects.all()
    serializer_class = WarningSerializer


@api_view(["GET"])
def warnings_by_location(request):
    """
    API endpoint to get current IMGW warnings for a specific location.

    This endpoint uses latitude and longitude from query parameters to find the
    corresponding TERYT county code. It then filters warnings to find those
    that are currently active and match that TERYT code.

    Args:
        request (HttpRequest): The request object containing 'lat' and 'lon'
                               as query parameters.

    Returns:
        Response: A JSON response with the TERYT code and a list of matching
                  warnings, or an error if the county cannot be found.
    """

    serializer = LocationQuerySerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)

    lat = serializer.validated_data["lat"]
    lon = serializer.validated_data["lon"]

    teryt = get_teryt_from_coords(lat, lon)
    if not teryt:
        return Response({"error": "Cant find county for given coordinates"}, status=404)

    now = timezone.now()

    qs = Warning.objects.filter(areas__contains=[teryt], start__lte=now, end__gte=now)

    warnings_data = WarningSerializer(qs, many=True).data

    return Response({"teryt": teryt, "warnings": warnings_data})
