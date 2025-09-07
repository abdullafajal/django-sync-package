
from django.core.management.base import BaseCommand
from sync.services import SyncService

class Command(BaseCommand):
    help = 'Syncs data between master and slave databases'

    def add_arguments(self, parser):
        parser.add_argument(
            '--direction',
            type=str,
            default='master-to-slave',
            choices=['master-to-slave', 'slave-to-master'],
            help='Sync direction: "master-to-slave" or "slave-to-master"',
        )

    def handle(self, *args, **options):
        direction = options['direction']

        self.stdout.write(self.style.SUCCESS(f'Starting data synchronization ({direction})...'))
        sync_service = SyncService()
        sync_service.sync_data(direction=direction)
        self.stdout.write(self.style.SUCCESS('Data synchronization finished.'))
