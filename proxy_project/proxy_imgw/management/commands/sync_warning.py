from django.core.management.base import BaseCommand
from proxy_imgw.sync_imgw_warnings import CommandManager


command_manager = CommandManager()


class Command(BaseCommand):
    help = 'Synchronizes IMGW warnings from the API.'

    def handle(self, *args, **options):
        """
        The main entry point for the Django management command.

        This method initiates the synchronization process by calling the
        `command_manager.handle()` method, which fetches, processes, and
        stores meteorological warnings from the IMGW API. It provides
        console output for the start and successful completion of the
        synchronization.
        """

        self.stdout.write("Starting synchronization...")
        command_manager.handle()
        self.stdout.write(self.style.SUCCESS("Synchronization finished successfully!"))