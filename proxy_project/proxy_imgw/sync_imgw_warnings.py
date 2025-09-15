import requests
from dateutil import parser as dtparser
from django.core.management.base import BaseCommand
from proxy.models import Warning


IMGW_URL = 'https://danepubliczne.imgw.pl/api/data/warningsmeteo'


class IMGWFetcher:
    """Fetches raw meteorological warning data from the IMGW API."""

    def fetch_warnings(self):
        """
        Fetches raw warning data from the IMGW API.

        This method sends an HTTP GET request to the IMGW API and returns the
        parsed JSON data. It includes a timeout and handles potential request
        exceptions gracefully by printing an error message and returning an
        empty list.

        Returns:
            list: A list of warning data dictionaries if the request is
                  successful, otherwise an empty list.
        """
        try:
            r = requests.get(IMGW_URL, timeout=20)
            r.raise_for_status()
            data = r.json()

            return data if isinstance(data, list) else data.get('warnings', []) if isinstance(data, dict) else []
        except requests.RequestException as e:
            print(f"Encountered an error during the fetch of data from IMGW API: {e}")
            return []


class WarningProcessor:
    """Processes raw IMGW warning data into a standardized dictionary."""

    def process_item(self, item):
        """
        Processes a single IMGW data item into a standardized dictionary.

        This method maps the keys from the raw IMGW data to a predefined set
        of standardized keys, making the data easier to work with. It also
        stores the original raw data for reference.

        Args:
            item (dict): A single dictionary of raw warning data from IMGW.

        Returns:
            dict: A standardized dictionary containing processed warning data.
        """

        return {
            'imgw_id': str(item.get('id') or item.get('symbol') or item.get('uuid')),
            'title': item.get('nazwa_zdarzenia'),
            'level': item.get('stopien'),
            'possibility': item.get('prawdopodobienstwo'),
            'start': item.get('obowiazuje_od'),
            'end': item.get('obowiazuje_do'),
            'published': item.get('opublikowano'),
            'description': item.get('tresc'),
            'comment': item.get('komentarz'),
            'office': item.get('biuro'),
            'areas': item.get('teryt'),

            'raw': item,
        }


class WarningService:
    """Handles the insertion or updating of warnings in the database."""

    def upsert_warning(self, processed_data):
        """
        Inserts or updates a single warning in the database.

        This method uses `imgw_id` to uniquely identify warnings. If an `imgw_id`
        is present, it uses `update_or_create`. If it's not available, it
        falls back to querying by `title` and `start` time to find and update
        existing records or create a new one if no match is found.

        Args:
            processed_data (dict): The standardized warning data dictionary.

        Returns:
            bool: True if a new warning was created, False if an existing one
                  was updated.
        """

        if processed_data['imgw_id'] and processed_data['imgw_id'] != 'None':
            obj, created = Warning.objects.update_or_create(
                imgw_id=processed_data['imgw_id'],
                defaults=processed_data
            )
            return created
        else:
            qs = Warning.objects.filter(title=processed_data['title'], start=processed_data['start'])
            if qs.exists():
                w = qs.first()
                for key, value in processed_data.items():
                    setattr(w, key, value)
                w.save()
                return False  # Updated
            else:
                Warning.objects.create(**processed_data)
                return True  # Inserted


class CommandManager(BaseCommand):
    """
    A Django management command to fetch and store IMGW warnings.

    This command orchestrates the entire process: fetching raw data, processing
    it, and then either inserting new warnings or updating existing ones in
    the database.
    """

    help = 'Fetch current meteorological warnings from IMGW and store them in db'

    def handle(self, *args, **options):
        """
        The main entry point for the management command.

        This method is executed when the command is run. It initializes the
        necessary classes, fetches data, processes each item, and then
        calls the service to upsert the data into the database. Finally, it
        reports the number of inserted and updated records.
        """

        self.stdout.write('Fetching IMGW warnings...')

        fetcher = IMGWFetcher()
        processor = WarningProcessor()
        service = WarningService()

        raw_warnings = fetcher.fetch_warnings()

        inserted = 0
        updated = 0

        for item in raw_warnings:
            processed_data = processor.process_item(item)
            is_created = service.upsert_warning(processed_data)

            if is_created:
                inserted += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f'Inserted: {inserted}, Updated: {updated}'))
