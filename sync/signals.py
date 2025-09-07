
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .services import SyncService

@receiver(post_save)
def sync_on_save(sender, instance, **kwargs):
    if sender._meta.label in settings.SYNC_CONFIG.get('MODELS', []):
        sync_service = SyncService()
        sync_service.sync_model(sender)

@receiver(post_delete)
def sync_on_delete(sender, instance, **kwargs):
    if sender._meta.label in settings.SYNC_CONFIG.get('MODELS', []):
        sync_service = SyncService()
        sync_service.sync_model(sender)
