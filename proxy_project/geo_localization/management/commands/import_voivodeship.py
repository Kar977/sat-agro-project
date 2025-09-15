from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource, CoordTransform, SpatialReference
from django.contrib.gis.geos import MultiPolygon, Polygon
from geo_localization.models import Voivodeship


class Command(BaseCommand):
    help = "Import boundaries of voivodeship from GML (EPSG:2180) file"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)

    def handle(self, *args, **options):
        file = options["file"]
        ds = DataSource(file)
        layer = ds[0]

        # Transformacja z EPSG:2180 do WGS84 (EPSG:4326)
        src_srs = SpatialReference(2180)
        dst_srs = SpatialReference(4326)
        transform = CoordTransform(src_srs, dst_srs)

        for feature in layer:
            name = feature.get("JPT_NAZWA") or feature.get("NAZWA") or "unknown"

            geom = feature.geom.geos  # geometria jako GEOS
            geom.transform(transform)  # przekształć do WGS84

            if isinstance(geom, Polygon):
                geom = MultiPolygon(geom)

            Voivodeship.objects.create(name=name, boundaries=geom)

        self.stdout.write(self.style.SUCCESS("Imported voivodeships from .GML"))
