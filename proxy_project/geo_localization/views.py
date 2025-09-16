from django.contrib.gis.geos import Point
from geo_localization.models import County


def get_teryt_from_coords(lat, lon):
    """
    Translates lat/lon coordinates to a TERYT county code.

    Args:
        lat: The latitude.
        lon: The longitude.

    Returns:
        The TERYT code (str) if a county is found, otherwise None.
    """
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return None

    # WGS84
    point = Point(lon, lat, srid=4326)
    # SRID (2180)
    point.transform(2180)

    county = County.objects.filter(boundaries__contains=point).first()
    return county.teryt if county else None
