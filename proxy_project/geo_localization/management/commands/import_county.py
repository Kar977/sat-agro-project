from django.contrib.gis.geos import MultiPolygon, Polygon
from django.core.management.base import BaseCommand
from geo_localization.models import County
from lxml import etree


class Command(BaseCommand):
    """
    Django management command to import county boundaries from a GML file.

    This command parses a GML file to extract polygon coordinates and saves them
    as a MultiPolygon object in the `County` model. It requires the file path,
    TERYT code, and county name as arguments.
    """

    help = "Import county from GML file"

    def add_arguments(self, parser):
        """
        Adds command-line arguments for the GML file path, TERYT code, and name.
        """
        parser.add_argument("gml_file", type=str)
        parser.add_argument(
            "--teryt", type=str, help="Teryt code ex. 0401", required=True
        )
        parser.add_argument("--name", type=str, help="County name", required=True)

    def handle(self, *args, **options):
        """
        The main logic of the command.

        This method reads a GML file, extracts all polygon coordinates (assuming EPSG:2180 X Y pairs),
        creates a MultiPolygon from them, and then uses `update_or_create` to save the county
        data to the database.
        """

        file_path = options["gml_file"]
        teryt = options["teryt"]
        name = options["name"]

        tree = etree.parse(file_path)
        ns = {"gml": "http://www.opengis.net/gml/3.2"}

        polygons = []
        for posList in tree.xpath(
            "//gml:Polygon/gml:exterior/gml:LinearRing/gml:posList", namespaces=ns
        ):
            coords_text = posList.text.strip()
            coords_pairs = coords_text.split()
            # EPSG:2180 -> pary X Y
            coords = [
                (float(coords_pairs[i]), float(coords_pairs[i + 1]))
                for i in range(0, len(coords_pairs), 2)
            ]

            poly = Polygon(coords)
            polygons.append(poly)

        if polygons:
            mp = MultiPolygon(polygons)
            County.objects.update_or_create(
                teryt=teryt, defaults={"name": name, "boundaries": mp}
            )
            self.stdout.write(self.style.SUCCESS(f"Imported {name}"))
        else:
            self.stdout.write(self.style.WARNING("Can't find geometry"))
