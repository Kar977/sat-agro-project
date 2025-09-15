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

    name = models.CharField(max_length=100, unique=True)
    boundaries = gis_models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name