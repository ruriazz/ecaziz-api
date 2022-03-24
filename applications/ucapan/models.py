import datetime
from django.db import models
from core.utils.models import ModelManager

from applications.undangan.models import Undangan

# TODO: models.ucapan
class Ucapan(models.Model):
    class Meta:
        managed = True
        db_table = 'ucapan'

    id = models.AutoField(primary_key=True)
    undangan = models.ForeignKey(Undangan, on_delete=models.CASCADE)
    sender = models.CharField(max_length=150)
    text = models.TextField(max_length=1000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    objects = ModelManager()
    default_objects = models.Manager()

    def soft_delete(self):
        self.is_active = False
        self.is_deleted = True
        self.deleted_at = datetime.datetime.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()