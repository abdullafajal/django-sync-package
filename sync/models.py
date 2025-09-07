from django.db import models

class SyncLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    object_id = models.CharField(max_length=255)
    object_repr = models.CharField(max_length=255)
    change_details = models.JSONField()
    source = models.CharField(max_length=255)
    winner = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.object_repr} synced at {self.timestamp}'