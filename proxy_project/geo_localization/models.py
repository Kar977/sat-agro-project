from django.contrib.gis.db import models as gis_models
from django.db import models


class County(models.Model):
    """
    A Django model to store information about administrative counties.

    Each county has a unique name and a geographical boundary represented by a
    MultiPolygonField. The srid=4326 indicates that the coordinates are
    in the WGS 84 spatial reference system (latitude and longitude).

    Attributes:
        name (str): The unique name of the county.
        boundaries (MultiPolygonField): The geographical boundaries of the county.
    """

    teryt = gis_models.CharField(max_length=4, unique=True)
    name = gis_models.CharField(max_length=255)
    boundaries = gis_models.MultiPolygonField(srid=2180)

    def __str__(self):
        return self.name
