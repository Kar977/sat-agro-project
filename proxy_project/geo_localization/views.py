from django.contrib.gis.geos import Point
from django.http import JsonResponse
from geo_localization.models import County

from proxy_project.proxy_project.constants import COUNTY_DICT


def get_county(point):
    """
    Retrieves the name of the county containing a given geographical point.

    This function performs a spatial lookup in the database to find a `County` object
    whose boundaries contain the specified point. It returns the name of the first
    matching county found, or None if no county is found.

    Args:
        point (django.contrib.gis.geos.Point): The geographical point to check,
                                               e.g. a user's location.

    Returns:
        str or None: The name of the county if found, otherwise None.
    """

    county = County.objects.filter(boundaries__contains=point).first()

    if county:
        return county.name
    else:
        return None


def get_teryt(request):
    """
    API endpoint to get the TERYT code for a given latitude and longitude.

    This view function expects 'lat' and 'lon' as GET query parameters. It creates a
    `Point` object from these coordinates, determines the containing county using
    `get_county`, and then looks up the corresponding TERYT code from a dictionary.
    It returns the TERYT code as a JSON response.

    Args:
        request (HttpRequest): The HTTP request object. Expected to contain 'lat'
                               and 'lon' in its query parameters.

    Returns:
        JsonResponse: A JSON response containing the TERYT code for the location,
                      or null if the county is not found.
                      Example: {"teryt": "0213"}
    """

    lat = float(request.GET.get('lat'))
    lon = float(request.GET.get('lon'))
    point = Point(lon, lat, srid=4326)
    county_name = get_county(point)

    return JsonResponse({"teryt": COUNTY_DICT.get(county_name)})




