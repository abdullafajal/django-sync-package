
from django.conf import settings
from django.apps import apps
from django.db import connections, router
from .models import SyncLog

class SyncService:
    def __init__(self):
        self.master_db = 'default'
        self.slave_db = 'slave'
        self.models_to_sync = settings.SYNC_CONFIG.get('MODELS', [])

    def sync_data(self, direction='master-to-slave'):
        if direction == 'master-to-slave':
            source_db = self.master_db
            dest_db = self.slave_db
        elif direction == 'slave-to-master':
            source_db = self.slave_db
            dest_db = self.master_db
        else:
            raise ValueError("Invalid direction. Use 'master-to-slave' or 'slave-to-master'.")

        for model_label in self.models_to_sync:
            model = apps.get_model(model_label)
            self.sync_model(model, source_db, dest_db)

    def sync_model(self, model, source_db, dest_db):
        source_queryset = model.objects.using(source_db).all()
        dest_queryset = model.objects.using(dest_db).all()

        source_objects = {obj.pk: obj for obj in source_queryset}
        dest_objects = {obj.pk: obj for obj in dest_queryset}

        # Sync from source to destination (create/update)
        for pk, source_obj in source_objects.items():
            dest_obj = dest_objects.get(pk)
            action = ''
            if not dest_obj:
                action = f'created_on_{dest_db}'
                self.copy_object(source_obj, dest_db)
            elif self.has_changed(source_obj, dest_obj):
                action = f'updated_on_{dest_db}'
                self.copy_object(source_obj, dest_db)

            if action:
                SyncLog.objects.using(self.master_db).create(
                    object_id=source_obj.pk,
                    object_repr=str(source_obj),
                    change_details={'action': action},
                    source=source_db,
                    winner=source_db
                )

        # Sync from source to destination (delete)
        for pk, dest_obj in dest_objects.items():
            if pk not in source_objects:
                action = f'deleted_from_{dest_db}'
                object_id = dest_obj.pk
                object_repr = str(dest_obj)
                self.delete_object(dest_obj)
                SyncLog.objects.using(self.master_db).create(
                    object_id=object_id,
                    object_repr=object_repr,
                    change_details={'action': action},
                    source=source_db,
                    winner=source_db
                )

    def copy_object(self, obj, dest_db):
        obj.save(using=dest_db)

    def delete_object(self, obj):
        obj.delete()

    def has_changed(self, obj1, obj2):
        excluded_fields = settings.SYNC_CONFIG.get('EXCLUDE', {}).get(obj1._meta.label, [])
        for field in obj1._meta.fields:
            if field.name in excluded_fields:
                continue
            if getattr(obj1, field.name) != getattr(obj2, field.name):
                return True
        return False
