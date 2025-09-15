from django.utils import timezone
from geo_localization.views import get_teryt_from_coords
from proxy_imgw.models import Warning


def get_warnings_for_location(lat, lon):
    """
    Fetches active meteorological warnings for a given geographical location.

    This function first determines the TERYT code (county identifier) for the provided
    latitude and longitude. It then queries the database for all currently active
    warnings that apply to that specific TERYT code.

    Args:
        lat (float): The latitude of the location.
        lon (float): The longitude of the location.

    Returns:
        tuple[str | None, QuerySet]: A tuple containing:
            - The TERYT code (str) if a county is found, otherwise None.
            - A Django QuerySet of active `Warning` objects for that TERYT code.
              Returns an empty QuerySet if no county is found.
    """
    teryt = get_teryt_from_coords(lat, lon)
    if not teryt:
        return None, Warning.objects.none()

    now = timezone.now()
    qs = Warning.objects.filter(areas__contains=[teryt], start__lte=now, end__gte=now)
    return teryt, qs
